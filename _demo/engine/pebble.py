"""
Pebble data model — a Universal Knowledge Unit (UKU).

Each pebble is a Markdown file with YAML frontmatter that captures
both raw content and experiential metadata at the moment of creation.
"""

import hashlib
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional


def generate_uku_id() -> str:
    """Generate a unique UKU identifier: uku-YYYYMMDD-hex."""
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    hex_str = uuid.uuid4().hex[:12]
    return f"uku-{date_str}-{hex_str}"


def content_hash(text: str) -> str:
    """SHA-256 hash of body content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass
class ContextElements:
    why_captured: Optional[str] = None
    surrounding_activity: Optional[str] = None
    emotional_state: Optional[str] = None
    intended_next_action: Optional[str] = None


@dataclass
class LocationData:
    name: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    type: Optional[str] = None  # e.g. "coffee_shop", "library", "home"


@dataclass
class ConsentSnapshot:
    """Captures opt-in consent state for all nearby people at creation time."""
    consented_people: list = field(default_factory=list)
    consent_type: str = "explicit_opt_in"
    timestamp: Optional[str] = None


@dataclass
class BookReference:
    """Reference to full content for drill-down."""
    book_title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    chapter: Optional[str] = None
    chapter_number: Optional[int] = None
    page: Optional[int] = None
    paragraph: Optional[int] = None
    section: Optional[str] = None


@dataclass
class Pebble:
    # Required fields
    title: str = ""
    uku_id: str = field(default_factory=generate_uku_id)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    uku_type: str = "experience_capture"
    category: str = "insight"

    # Standard optional fields
    url: Optional[str] = None
    source_id: Optional[str] = None
    tags: list = field(default_factory=list)
    weight: Optional[float] = None
    status: str = "draft"

    # Experiential metadata
    context_elements: Optional[ContextElements] = None

    # Location (fluid field for book-reading use case)
    location: Optional[LocationData] = None

    # People present (all must opt in)
    people: list = field(default_factory=list)
    consent_snapshot: Optional[ConsentSnapshot] = None

    # Book reference for drill-down
    book_ref: Optional[BookReference] = None

    # Source app
    source_app: Optional[str] = None

    # Content hash
    content_hash: Optional[str] = None

    # Clearance level (0-4)
    clearance_level: int = 0

    # Domain tag
    domain_tag: Optional[str] = None

    # The actual highlight / body text
    body: str = ""

    # Sharing permissions
    shared_with: list = field(default_factory=list)
    shared_with_groups: list = field(default_factory=list)

    # Creator
    creator: Optional[str] = None

    def to_yaml_dict(self):
        """Convert to a dict suitable for YAML frontmatter (excludes body)."""
        d = {}
        for k, v in asdict(self).items():
            if k == "body":
                continue
            if v is None or v == [] or v == {}:
                continue
            d[k] = v
        return d

    def to_markdown(self) -> str:
        """Render as a full Markdown file with YAML frontmatter."""
        import yaml

        yaml_dict = self.to_yaml_dict()
        front = yaml.dump(yaml_dict, default_flow_style=False, sort_keys=False)
        return f"---\n{front}---\n\n{self.body}\n"

    @classmethod
    def from_markdown(cls, text: str) -> "Pebble":
        """Parse a Markdown file with YAML frontmatter into a Pebble."""
        import frontmatter

        post = frontmatter.loads(text)
        meta = dict(post.metadata)

        # Reconstruct nested dataclasses
        if "context_elements" in meta and isinstance(meta["context_elements"], dict):
            meta["context_elements"] = ContextElements(**meta["context_elements"])
        if "location" in meta and isinstance(meta["location"], dict):
            meta["location"] = LocationData(**meta["location"])
        if "consent_snapshot" in meta and isinstance(meta["consent_snapshot"], dict):
            meta["consent_snapshot"] = ConsentSnapshot(**meta["consent_snapshot"])
        if "book_ref" in meta and isinstance(meta["book_ref"], dict):
            meta["book_ref"] = BookReference(**meta["book_ref"])

        meta["body"] = post.content
        return cls(**meta)
