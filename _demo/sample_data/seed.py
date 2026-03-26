"""
Seed script — creates realistic sample pebbles for the book-reading demo.

Scenario: A person reading "Meditations" by Marcus Aurelius over several weeks
at various locations, with friends sometimes present (all opted in).
Demonstrates the full spectrum of UKU YAML attributes.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.pebble import (
    Pebble, ContextElements, LocationData, ConsentSnapshot, BookReference, content_hash,
)
from engine.store import init_db, store_pebble

# === Constants ===

BOOK = BookReference(
    book_title="Meditations",
    author="Marcus Aurelius",
    isbn="978-0140449334",
)

CREATOR = "luke"


def make_pebbles() -> list[Pebble]:
    pebbles = []

    # --- Highlight 1: Coffee shop, two weeks ago, with Sarah ---
    p = Pebble(
        title="The impediment to action advances action",
        uku_id="uku-20260312-a1b2c3d4e5f6",
        created_at="2026-03-12T09:15:00Z",
        uku_type="experience_capture",
        category="insight",
        tags=["stoicism", "resilience", "obstacles", "reading", "marcus-aurelius"],
        weight=0.9,
        status="annotated",
        context_elements=ContextElements(
            why_captured="This hit hard — exactly what I needed to hear about the project setback",
            surrounding_activity="Reading at Blue Bottle Coffee, morning routine",
            emotional_state="inspired",
            intended_next_action="Apply this framing to the product launch delay",
        ),
        location=LocationData(
            name="Blue Bottle Coffee, Hayes Valley",
            lat=37.7764,
            lon=-122.4216,
            type="coffee_shop",
        ),
        people=["sarah"],
        consent_snapshot=ConsentSnapshot(
            consented_people=["sarah"],
            consent_type="explicit_opt_in",
            timestamp="2026-03-12T09:14:00Z",
        ),
        book_ref=BookReference(
            book_title="Meditations",
            author="Marcus Aurelius",
            isbn="978-0140449334",
            chapter="Book V",
            chapter_number=5,
            page=67,
            paragraph=20,
            section="On Obstacles",
        ),
        source_app="uku-reader",
        clearance_level=0,
        domain_tag="philosophy",
        creator=CREATOR,
        shared_with=["sarah"],
        shared_with_groups=["book-club"],
        body="""\"The impediment to action advances action. What stands in the way becomes the way.\"

This is the core Stoic insight about obstacles. Every setback contains within it
the seed of an equal or greater benefit — not through magical thinking, but because
the *response* to the obstacle is itself the practice of virtue.

Reading this while dealing with the Q2 product delay. The delay IS the opportunity
to rebuild the architecture properly. Marcus would approve.
""",
    )
    p.content_hash = content_hash(p.body)
    pebbles.append(p)

    # --- Highlight 2: Same coffee shop, same day, later ---
    p = Pebble(
        title="You have power over your mind, not outside events",
        uku_id="uku-20260312-b2c3d4e5f6a7",
        created_at="2026-03-12T09:42:00Z",
        uku_type="experience_capture",
        category="foundational",
        tags=["stoicism", "mindset", "control", "reading", "marcus-aurelius"],
        weight=0.85,
        status="annotated",
        context_elements=ContextElements(
            why_captured="The distinction between what we control and what we don't — foundational",
            surrounding_activity="Reading at Blue Bottle Coffee, second espresso",
            emotional_state="contemplative",
            intended_next_action="Journal about what I can and cannot control this quarter",
        ),
        location=LocationData(
            name="Blue Bottle Coffee, Hayes Valley",
            lat=37.7764,
            lon=-122.4216,
            type="coffee_shop",
        ),
        people=["sarah"],
        consent_snapshot=ConsentSnapshot(
            consented_people=["sarah"],
            consent_type="explicit_opt_in",
            timestamp="2026-03-12T09:14:00Z",
        ),
        book_ref=BookReference(
            book_title="Meditations",
            author="Marcus Aurelius",
            isbn="978-0140449334",
            chapter="Book VI",
            chapter_number=6,
            page=78,
            paragraph=8,
        ),
        source_app="uku-reader",
        clearance_level=0,
        domain_tag="philosophy",
        creator=CREATOR,
        shared_with=["sarah"],
        shared_with_groups=["book-club"],
        body="""\"You have power over your mind — not outside events. Realize this, and you will find strength.\"

The dichotomy of control. Everything in Stoicism flows from this one idea.
Sarah and I discussed this over coffee — she connected it to her meditation practice.
She said it's the same insight but from a different door.

This is the bridge between Stoicism and mindfulness. Same truth, different vocabulary.
""",
    )
    p.content_hash = content_hash(p.body)
    pebbles.append(p)

    # --- Highlight 3: Library, 10 days ago ---
    p = Pebble(
        title="Waste no more time arguing about what a good man should be",
        uku_id="uku-20260316-c3d4e5f6a7b8",
        created_at="2026-03-16T14:30:00Z",
        uku_type="insight",
        category="insight",
        tags=["stoicism", "action", "virtue", "reading", "marcus-aurelius"],
        weight=0.95,
        status="published",
        context_elements=ContextElements(
            why_captured="This is the ultimate call to action — stop theorizing, start doing",
            surrounding_activity="Reading at SF Public Library, quiet afternoon",
            emotional_state="challenged",
            intended_next_action="Share with the team as a rallying cry",
        ),
        location=LocationData(
            name="San Francisco Public Library",
            lat=37.7785,
            lon=-122.4156,
            type="library",
        ),
        people=[],
        book_ref=BookReference(
            book_title="Meditations",
            author="Marcus Aurelius",
            isbn="978-0140449334",
            chapter="Book X",
            chapter_number=10,
            page=142,
            paragraph=16,
        ),
        source_app="uku-reader",
        clearance_level=0,
        domain_tag="philosophy",
        creator=CREATOR,
        shared_with_groups=["book-club", "engineering-team"],
        body="""\"Waste no more time arguing about what a good man should be. Be one.\"

The shortest and most devastating passage in the entire book.
All the philosophy, all the frameworks, all the debates — they mean nothing
without action. Marcus wrote this as a *reminder to himself*, the most
powerful man in the known world, that even he was procrastinating.

I'm going to print this and put it on my desk.
""",
    )
    p.content_hash = content_hash(p.body)
    pebbles.append(p)

    # --- Highlight 4: Home, 8 days ago, with partner ---
    p = Pebble(
        title="The soul becomes dyed with the color of its thoughts",
        uku_id="uku-20260318-d4e5f6a7b8c9",
        created_at="2026-03-18T21:15:00Z",
        uku_type="experience_capture",
        category="foundational",
        tags=["stoicism", "mindset", "thoughts", "reading", "marcus-aurelius", "psychology"],
        weight=0.8,
        status="annotated",
        context_elements=ContextElements(
            why_captured="Connection between ancient wisdom and modern cognitive behavioral therapy",
            surrounding_activity="Reading in bed, evening wind-down",
            emotional_state="contemplative",
            intended_next_action="Research CBT connection to Stoicism",
        ),
        location=LocationData(
            name="Home",
            lat=37.7749,
            lon=-122.4194,
            type="home",
        ),
        people=["alex"],
        consent_snapshot=ConsentSnapshot(
            consented_people=["alex"],
            consent_type="explicit_opt_in",
            timestamp="2026-03-18T21:10:00Z",
        ),
        book_ref=BookReference(
            book_title="Meditations",
            author="Marcus Aurelius",
            isbn="978-0140449334",
            chapter="Book V",
            chapter_number=5,
            page=62,
            paragraph=16,
            section="On the Mind",
        ),
        source_app="uku-reader",
        clearance_level=0,
        domain_tag="philosophy",
        creator=CREATOR,
        shared_with=["alex"],
        body="""\"The soul becomes dyed with the color of its thoughts.\"

Alex pointed out this is basically the premise of CBT — your habitual
thought patterns literally shape your mental reality. Marcus figured this
out 2000 years before Aaron Beck.

The Stoics were the original cognitive therapists. This deserves a
deeper exploration — maybe a blog post connecting the two traditions.
""",
    )
    p.content_hash = content_hash(p.body)
    pebbles.append(p)

    # --- Highlight 5: Coffee shop again, 5 days ago, with Sarah and James ---
    p = Pebble(
        title="Never value anything as profitable that compels you to break your promise",
        uku_id="uku-20260321-e5f6a7b8c9d0",
        created_at="2026-03-21T10:00:00Z",
        uku_type="experience_capture",
        category="insight",
        tags=["stoicism", "integrity", "ethics", "reading", "marcus-aurelius", "leadership"],
        weight=0.85,
        status="annotated",
        context_elements=ContextElements(
            why_captured="James told a story about a business deal gone wrong — this passage was perfect",
            surrounding_activity="Book club meeting at Blue Bottle Coffee",
            emotional_state="excited",
            intended_next_action="Discuss ethics framework at next team standup",
        ),
        location=LocationData(
            name="Blue Bottle Coffee, Hayes Valley",
            lat=37.7764,
            lon=-122.4216,
            type="coffee_shop",
        ),
        people=["sarah", "james"],
        consent_snapshot=ConsentSnapshot(
            consented_people=["sarah", "james"],
            consent_type="explicit_opt_in",
            timestamp="2026-03-21T09:58:00Z",
        ),
        book_ref=BookReference(
            book_title="Meditations",
            author="Marcus Aurelius",
            isbn="978-0140449334",
            chapter="Book I",
            chapter_number=1,
            page=12,
            paragraph=7,
        ),
        source_app="uku-reader",
        clearance_level=0,
        domain_tag="philosophy",
        creator=CREATOR,
        shared_with=["sarah", "james"],
        shared_with_groups=["book-club"],
        body="""\"Never value anything as profitable that compels you to break your promise,
to lose your self-respect, to hate any man, to suspect, to curse, to act the hypocrite,
to desire anything that needs walls or curtains.\"

James just told us about turning down a lucrative partnership because the
terms required him to mislead customers. This passage — written by a Roman
Emperor — validates that decision perfectly.

The group discussed: integrity isn't just a nice-to-have. Marcus argues
it's the *only* thing that's actually profitable in the long run.
""",
    )
    p.content_hash = content_hash(p.body)
    pebbles.append(p)

    # --- Highlight 6: Park, 3 days ago ---
    p = Pebble(
        title="Loss is nothing else but change, and change is Nature's delight",
        uku_id="uku-20260323-f6a7b8c9d0e1",
        created_at="2026-03-23T16:45:00Z",
        uku_type="insight",
        category="vision",
        tags=["stoicism", "change", "impermanence", "reading", "marcus-aurelius", "nature"],
        weight=0.75,
        status="draft",
        context_elements=ContextElements(
            why_captured="Watching leaves fall while reading about impermanence — perfect synchronicity",
            surrounding_activity="Reading on a bench in Golden Gate Park",
            emotional_state="peaceful",
            intended_next_action="Sit with this idea; no action needed",
        ),
        location=LocationData(
            name="Golden Gate Park, Conservatory of Flowers",
            lat=37.7694,
            lon=-122.4619,
            type="park",
        ),
        people=[],
        book_ref=BookReference(
            book_title="Meditations",
            author="Marcus Aurelius",
            isbn="978-0140449334",
            chapter="Book IX",
            chapter_number=9,
            page=128,
            paragraph=35,
        ),
        source_app="uku-reader",
        clearance_level=0,
        domain_tag="philosophy",
        creator=CREATOR,
        shared_with_groups=["book-club"],
        body="""\"Loss is nothing else but change, and change is Nature's delight.\"

Sitting in the park watching leaves fall. The timing of reading this
couldn't be more perfect. Everything around me is demonstrating this truth.

This connects to the Buddhist concept of impermanence (anicca).
Marcus would have gotten along well with the Buddha.
""",
    )
    p.content_hash = content_hash(p.body)
    pebbles.append(p)

    # --- Highlight 7: Transit, yesterday ---
    p = Pebble(
        title="Think of the life you have lived as already dead",
        uku_id="uku-20260325-a7b8c9d0e1f2",
        created_at="2026-03-25T08:20:00Z",
        uku_type="experience_capture",
        category="foundational",
        tags=["stoicism", "mortality", "perspective", "reading", "marcus-aurelius", "memento-mori"],
        weight=0.7,
        status="draft",
        context_elements=ContextElements(
            why_captured="Memento mori on the morning commute — stark but motivating",
            surrounding_activity="Reading on BART during morning commute",
            emotional_state="contemplative",
            intended_next_action="Remember this feeling when tempted to waste time",
        ),
        location=LocationData(
            name="BART, 16th St Mission to Embarcadero",
            lat=37.7649,
            lon=-122.4194,
            type="transit",
        ),
        people=[],
        book_ref=BookReference(
            book_title="Meditations",
            author="Marcus Aurelius",
            isbn="978-0140449334",
            chapter="Book VII",
            chapter_number=7,
            page=94,
            paragraph=56,
        ),
        source_app="uku-reader",
        clearance_level=0,
        domain_tag="philosophy",
        creator=CREATOR,
        body="""\"Think of the life you have lived as already dead. See what is left as a bonus
and live it according to Nature.\"

Morning commute, packed train, everyone staring at their phones.
Marcus would say: every single one of these people has a finite number
of mornings left. Including me. Am I using mine well?

Heavy for 8am but that's the point.
""",
    )
    p.content_hash = content_hash(p.body)
    pebbles.append(p)

    # --- Insight 8: Sarah's shared pebble (from her perspective) ---
    p = Pebble(
        title="Stoicism meets mindfulness — same truth, different doors",
        uku_id="uku-20260312-s1a2r3a4h5b6",
        created_at="2026-03-12T10:05:00Z",
        uku_type="insight",
        category="insight",
        tags=["stoicism", "mindfulness", "meditation", "connection", "marcus-aurelius"],
        weight=0.9,
        status="published",
        context_elements=ContextElements(
            why_captured="Conversation with Luke sparked this — dichotomy of control IS non-attachment",
            surrounding_activity="Discussing Meditations at Blue Bottle Coffee",
            emotional_state="inspired",
            intended_next_action="Write a comparison post for the book club",
        ),
        location=LocationData(
            name="Blue Bottle Coffee, Hayes Valley",
            lat=37.7764,
            lon=-122.4216,
            type="coffee_shop",
        ),
        people=["luke"],
        consent_snapshot=ConsentSnapshot(
            consented_people=["luke"],
            consent_type="explicit_opt_in",
            timestamp="2026-03-12T10:04:00Z",
        ),
        book_ref=BookReference(
            book_title="Meditations",
            author="Marcus Aurelius",
            isbn="978-0140449334",
            chapter="Book VI",
            chapter_number=6,
            page=78,
        ),
        source_app="uku-reader",
        clearance_level=0,
        domain_tag="philosophy",
        creator="sarah",
        shared_with=["luke"],
        shared_with_groups=["book-club"],
        body="""Luke and I were reading the passage about power over the mind, and it clicked:

The Stoic \"dichotomy of control\" is the Western version of Buddhist non-attachment.
Both traditions say: suffering comes from clinging to what you can't control.

Marcus says: focus on what's in your power (your mind, your choices).
Buddha says: let go of attachment to outcomes.

Same destination, different maps. I want to explore this connection more deeply.
""",
    )
    p.content_hash = content_hash(p.body)
    pebbles.append(p)

    # --- Insight 9: James's shared pebble ---
    p = Pebble(
        title="Integrity as competitive advantage — Marcus Aurelius in business",
        uku_id="uku-20260321-j1a2m3e4s5b6",
        created_at="2026-03-21T11:30:00Z",
        uku_type="proposed_solution",
        category="insight",
        tags=["stoicism", "business", "ethics", "integrity", "leadership", "marcus-aurelius"],
        weight=0.8,
        status="published",
        context_elements=ContextElements(
            why_captured="The book club discussion crystallized why I turned down that deal",
            surrounding_activity="Post-book-club reflection at Blue Bottle Coffee",
            emotional_state="validated",
            intended_next_action="Draft an internal memo on ethical decision-making",
        ),
        location=LocationData(
            name="Blue Bottle Coffee, Hayes Valley",
            lat=37.7764,
            lon=-122.4216,
            type="coffee_shop",
        ),
        people=["luke", "sarah"],
        consent_snapshot=ConsentSnapshot(
            consented_people=["luke", "sarah"],
            consent_type="explicit_opt_in",
            timestamp="2026-03-21T09:58:00Z",
        ),
        book_ref=BookReference(
            book_title="Meditations",
            author="Marcus Aurelius",
            isbn="978-0140449334",
            chapter="Book I",
            chapter_number=1,
            page=12,
        ),
        source_app="uku-reader",
        clearance_level=0,
        domain_tag="business-philosophy",
        creator="james",
        shared_with=["luke", "sarah"],
        shared_with_groups=["book-club"],
        body="""After today's book club discussion, I'm more convinced than ever:

Turning down the Meridian partnership was the right call. Marcus Aurelius
didn't write \"never value anything as profitable that compels you to break
your promise\" as abstract philosophy — he wrote it as a *decision framework*.

Proposed framework for the team:
1. Does this require us to mislead anyone? → No go
2. Would we be comfortable if this was public? → Transparency test
3. Does this build long-term trust? → Relationship test

Short-term profit < Long-term integrity. Always.
""",
    )
    p.content_hash = content_hash(p.body)
    pebbles.append(p)

    # --- Highlight 10: Different book for cross-reference ---
    p = Pebble(
        title="Between stimulus and response there is a space",
        uku_id="uku-20260310-v1i2k3t4o5r6",
        created_at="2026-03-10T19:30:00Z",
        uku_type="experience_capture",
        category="foundational",
        tags=["psychology", "mindset", "freedom", "reading", "viktor-frankl"],
        weight=0.95,
        status="published",
        context_elements=ContextElements(
            why_captured="The most important sentence ever written about human freedom",
            surrounding_activity="Reading at home, evening",
            emotional_state="moved",
            intended_next_action="Connect this to the Meditations passages about the mind",
        ),
        location=LocationData(
            name="Home",
            lat=37.7749,
            lon=-122.4194,
            type="home",
        ),
        people=["alex"],
        consent_snapshot=ConsentSnapshot(
            consented_people=["alex"],
            consent_type="explicit_opt_in",
            timestamp="2026-03-10T19:25:00Z",
        ),
        book_ref=BookReference(
            book_title="Man's Search for Meaning",
            author="Viktor Frankl",
            isbn="978-0807014295",
            chapter="Experiences in a Concentration Camp",
            page=75,
        ),
        source_app="uku-reader",
        clearance_level=0,
        domain_tag="psychology",
        creator=CREATOR,
        shared_with=["alex"],
        body="""\"Between stimulus and response there is a space. In that space is our power
to choose our response. In our response lies our growth and our freedom.\"

This connects DIRECTLY to Marcus Aurelius — \"You have power over your mind,
not outside events.\" Frankl proved this in the most extreme conditions
imaginable. The Stoics theorized it; Frankl lived it.

Alex teared up when I read this aloud. Some truths hit different.
""",
    )
    p.content_hash = content_hash(p.body)
    pebbles.append(p)

    return pebbles


def seed():
    """Initialize the database and insert sample pebbles."""
    db_path = os.path.join(os.path.dirname(__file__), "..", "pebbles.db")
    # Remove existing DB for clean seed
    if os.path.exists(db_path):
        os.remove(db_path)

    init_db(db_path)

    pebbles = make_pebbles()
    for p in pebbles:
        store_pebble(p, db_path)

        # Also write as .md files to the vault
        vault_dir = os.path.join(os.path.dirname(__file__), "vault")
        filename = p.uku_id + ".md"
        filepath = os.path.join(vault_dir, filename)
        with open(filepath, "w") as f:
            f.write(p.to_markdown())

    print(f"Seeded {len(pebbles)} pebbles into {db_path}")
    print(f"Wrote {len(pebbles)} markdown files to sample_data/vault/")


if __name__ == "__main__":
    seed()
