"""
Natural language query → sub-agent structured queries.

Demonstrates translating vague human queries like:
  "show me the important insights I made in the book at the coffee shop two weeks ago"

Into one or more structured sub-agent queries against YAML attributes.
"""

import re
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SubAgentQuery:
    """A single structured query that maps to YAML attribute filters."""
    intent: str  # what this sub-query is looking for
    filters: dict = field(default_factory=dict)
    confidence: float = 1.0  # how confident we are in this interpretation


@dataclass
class ParsedQuery:
    """Result of parsing a natural language query into sub-agent queries."""
    original: str
    sub_queries: list = field(default_factory=list)
    explanation: str = ""


# Keyword → YAML attribute mapping
LOCATION_KEYWORDS = {
    "coffee shop": {"$.location.type": "coffee_shop"},
    "café": {"$.location.type": "coffee_shop"},
    "cafe": {"$.location.type": "coffee_shop"},
    "library": {"$.location.type": "library"},
    "home": {"$.location.type": "home"},
    "office": {"$.location.type": "office"},
    "park": {"$.location.type": "park"},
    "train": {"$.location.type": "transit"},
    "bus": {"$.location.type": "transit"},
    "airport": {"$.location.type": "airport"},
}

TYPE_KEYWORDS = {
    "insight": "insight",
    "insights": "insight",
    "highlight": "experience_capture",
    "highlights": "experience_capture",
    "note": "experience_capture",
    "notes": "experience_capture",
    "idea": "proposed_solution",
    "ideas": "proposed_solution",
    "problem": "problem_statement",
    "problems": "problem_statement",
    "question": "problem_statement",
    "questions": "problem_statement",
}

WEIGHT_KEYWORDS = {
    "important": 0.7,
    "significant": 0.7,
    "key": 0.8,
    "critical": 0.9,
    "favorite": 0.8,
    "best": 0.8,
    "top": 0.9,
}

EMOTION_KEYWORDS = {
    "excited": "excited",
    "happy": "happy",
    "frustrated": "frustrated",
    "curious": "curious",
    "inspired": "inspired",
    "surprised": "surprised",
    "thoughtful": "contemplative",
    "moved": "moved",
    "challenged": "challenged",
}

TIME_PATTERNS = [
    (r"(\d+)\s+days?\s+ago", lambda m: timedelta(days=int(m.group(1)))),
    (r"(\d+)\s+weeks?\s+ago", lambda m: timedelta(weeks=int(m.group(1)))),
    (r"(\d+)\s+months?\s+ago", lambda m: timedelta(days=int(m.group(1)) * 30)),
    (r"yesterday", lambda m: timedelta(days=1)),
    (r"last\s+week", lambda m: timedelta(weeks=1)),
    (r"last\s+month", lambda m: timedelta(days=30)),
    (r"two\s+weeks?\s+ago", lambda m: timedelta(weeks=2)),
    (r"three\s+weeks?\s+ago", lambda m: timedelta(weeks=3)),
    (r"this\s+week", lambda m: timedelta(days=datetime.now().weekday())),
    (r"today", lambda m: timedelta(days=0)),
]

ACTIVITY_KEYWORDS = {
    "reading": "reading",
    "book": "reading",
    "studying": "studying",
    "working": "working",
    "walking": "walking",
    "commuting": "commuting",
    "meeting": "meeting",
    "browsing": "browsing",
    "listening": "listening",
    "podcast": "listening",
}

PEOPLE_PATTERNS = [
    r"with\s+(\w+)",
    r"near\s+(\w+)",
    r"(?:and|,)\s+(\w+)\s+(?:were|was)\s+(?:there|nearby|present)",
]


def parse_query(text: str, reference_date: Optional[datetime] = None) -> ParsedQuery:
    """
    Parse a natural language query into structured sub-agent queries.

    Example:
      "show me the important insights I made in the book at the coffee shop two weeks ago"

    Produces sub-queries for:
      1. Time filter (created_at within ~2 weeks ago window)
      2. Location filter (location.type = coffee_shop)
      3. Type filter (uku_type = insight)
      4. Weight filter (weight >= 0.7 for "important")
      5. Activity filter (surrounding_activity LIKE reading)
    """
    if reference_date is None:
        reference_date = datetime.now(timezone.utc)

    lower = text.lower()
    sub_queries = []
    explanations = []

    # 1. Time extraction
    time_delta = None
    for pattern, delta_fn in TIME_PATTERNS:
        match = re.search(pattern, lower)
        if match:
            time_delta = delta_fn(match)
            break

    if time_delta is not None:
        target_date = reference_date - time_delta
        # Create a window: ±3 days around the target
        window_start = (target_date - timedelta(days=3)).isoformat()
        window_end = (target_date + timedelta(days=3)).isoformat()
        sub_queries.append(SubAgentQuery(
            intent="time_filter",
            filters={
                "$.created_at__gte": window_start,
                "$.created_at__lte": window_end,
            },
            confidence=0.85,
        ))
        explanations.append(f"Time: around {target_date.strftime('%Y-%m-%d')} (±3 days)")

    # 2. Location extraction
    for keyword, location_filter in LOCATION_KEYWORDS.items():
        if keyword in lower:
            sub_queries.append(SubAgentQuery(
                intent="location_filter",
                filters=location_filter,
                confidence=0.9,
            ))
            explanations.append(f"Location: {keyword}")
            break

    # Also check for specific place names (quoted or capitalized)
    place_match = re.search(r"(?:at|in)\s+(?:the\s+)?([A-Z][\w\s]+?)(?:\s+(?:two|three|last|this|yesterday)|\s*$|,)", text)
    if place_match:
        place_name = place_match.group(1).strip()
        if len(place_name) > 2:
            sub_queries.append(SubAgentQuery(
                intent="location_name_filter",
                filters={"$.location.name": place_name},
                confidence=0.7,
            ))
            explanations.append(f"Place name: {place_name}")

    # 3. Type extraction
    for keyword, uku_type in TYPE_KEYWORDS.items():
        if keyword in lower:
            sub_queries.append(SubAgentQuery(
                intent="type_filter",
                filters={"$.uku_type": uku_type},
                confidence=0.9,
            ))
            explanations.append(f"Type: {uku_type} (from '{keyword}')")
            break

    # 4. Weight / importance extraction
    for keyword, min_weight in WEIGHT_KEYWORDS.items():
        if keyword in lower:
            sub_queries.append(SubAgentQuery(
                intent="weight_filter",
                filters={"$.weight__gte": min_weight},
                confidence=0.8,
            ))
            explanations.append(f"Importance: weight >= {min_weight} (from '{keyword}')")
            break

    # 5. Activity extraction
    for keyword, activity in ACTIVITY_KEYWORDS.items():
        if keyword in lower:
            sub_queries.append(SubAgentQuery(
                intent="activity_filter",
                filters={"$.context_elements.surrounding_activity": activity},
                confidence=0.75,
            ))
            explanations.append(f"Activity: {activity} (from '{keyword}')")
            break

    # 6. Emotional state extraction
    for keyword, emotion in EMOTION_KEYWORDS.items():
        if keyword in lower:
            sub_queries.append(SubAgentQuery(
                intent="emotion_filter",
                filters={"$.context_elements.emotional_state": emotion},
                confidence=0.7,
            ))
            explanations.append(f"Emotion: {emotion}")
            break

    # 7. Tag extraction (look for hashtag-like words or specific domains)
    tag_matches = re.findall(r"#(\w+)", text)
    for tag in tag_matches:
        sub_queries.append(SubAgentQuery(
            intent="tag_filter",
            filters={"$.tags": tag},
            confidence=0.95,
        ))
        explanations.append(f"Tag: #{tag}")

    # 8. People extraction
    for pattern in PEOPLE_PATTERNS:
        match = re.search(pattern, lower)
        if match:
            person = match.group(1)
            # Filter out common words
            if person not in {"the", "a", "an", "my", "some", "any", "all"}:
                sub_queries.append(SubAgentQuery(
                    intent="people_filter",
                    filters={"$.people": person},
                    confidence=0.6,
                ))
                explanations.append(f"Person: {person}")

    # 9. Book-specific extraction — only match quoted titles or "book <Title>"
    book_match = re.search(r'(?:book|reading)\s+"([^"]+)"', lower)
    if not book_match:
        # Match capitalized book titles after "book" keyword
        book_match = re.search(r'(?:book|reading)\s+([A-Z][\w\s]+?)(?:\s+at|\s+in|\s+two|\s+last|\s+this|$)', text)
    if book_match:
        book_title = book_match.group(1).strip()
        # Filter out common phrases that aren't book titles
        noise = {"the", "and", "at the", "in the", "a", "some", "my", "this"}
        if book_title and len(book_title) > 2 and book_title.lower() not in noise:
            sub_queries.append(SubAgentQuery(
                intent="book_filter",
                filters={"$.book_ref.book_title": book_title},
                confidence=0.8,
            ))
            explanations.append(f"Book: {book_title}")

    explanation = "Decomposed query into sub-agent filters:\n" + "\n".join(
        f"  → {e}" for e in explanations
    ) if explanations else "No structured filters could be extracted."

    return ParsedQuery(
        original=text,
        sub_queries=sub_queries,
        explanation=explanation,
    )


def merge_filters(sub_queries: list[SubAgentQuery]) -> dict:
    """Merge all sub-query filters into a single filter dict for the store."""
    merged = {}
    for sq in sub_queries:
        merged.update(sq.filters)
    return merged


def format_query_plan(parsed: ParsedQuery) -> list[dict]:
    """Format the query plan for display — shows how NL maps to structured queries."""
    plan = []
    for sq in parsed.sub_queries:
        plan.append({
            "intent": sq.intent,
            "filters": sq.filters,
            "confidence": sq.confidence,
        })
    return plan
