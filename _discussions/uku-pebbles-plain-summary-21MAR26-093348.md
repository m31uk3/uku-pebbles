# What We Built and Why It Matters

```
     TODAY                              WITH UKU
  ┌──────────┐                    ┌──────────────────┐
  │  Image   │                    │  Image/Photo     │
  │          │                    │ ─────────────────│
  │  (just   │                    │  WHY you took it │
  │  pixels) │                    │  HOW you felt    │
  │          │                    │  WHAT to do next │
  └──────────┘                    │  WHO was there   │
                                  └──────────────────┘
  You remember.                   The file remembers.
  Until you don't.                Forever.


        ┌─────────┐
        │ YOU     │  ← capture a moment
        └────┬────┘
             │
             ▼
        ┌─────────┐
        │  UKU    │  ← your knowledge + your experience (universal schema)
        └────┬────┘
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
     SAGE  ByteRover AI
     checks  finds   uses
     it      it      it
```

## The Problem

When you take a photo, save a bookmark, or jot down a note, the tool saves *what* you captured — but it throws away everything else. It doesn't remember why you saved it, what you were doing at the time, how you were feeling, or what you planned to do with it later.

That "everything else" is often the most important part.

And it's even worse for AI assistants. Every time you start a new conversation with an AI, it has completely forgotten everything from last time. It's like talking to someone with amnesia — every session starts from zero.

## What We Did

We created a simple, open standard for saving knowledge in a way that keeps all that context attached — forever. The idea was [sparked by a conversation](../\_discussions/uku-pebbles-luke-aaron-box-21MAR26.md) about how context is the missing ingredient for AI agents.

Each piece of knowledge is called a **Universal Knowledge Unit (UKU)**. It's just a text file that anyone can open and read. But inside it, alongside the actual content, there's structured information about:

- **Why** you saved it
- **What you were doing** at the time
- **How you felt** about it
- **What you planned to do next**
- **Where you were**
- **How an AI assistant understands it** (filled in automatically)

Think of it like a photo that remembers not just what it looks like, but why you took it, who you were with, and what it meant to you.

## The Three Pieces

Three independent projects — built by different people who didn't know each other — discovered they were solving the same problem from different angles. They [found each other on X](../\_discussions/uku-pebbles-sage-byte-rover-21MAR26.md) and realized their work fits together perfectly:

1. **The Format ([UKU-Pebbles](../\_specs/uku-pebbles.spec.md))** — Defines *what* a knowledge unit looks like. The blueprint.
2. **The Validator ([SAGE](../\_research/sage/index.md))** — Makes sure the information stays accurate over time and doesn't get corrupted. Like a fact-checker that never sleeps.
3. **The Finder (ByteRover)** — Helps AI assistants find exactly the right piece of knowledge when they need it, instead of dumping everything at once.

No one planned this. Three people independently built three pieces that snap together like puzzle pieces. That's usually a sign the idea is right.

## Why It Matters

**For regular people:**
- Your notes, bookmarks, screenshots, and captures finally remember *why* they mattered to you — not just what they contain
- You own your data. It's stored as simple text files on your device. No company holds it hostage
- AI assistants can actually remember your preferences, your context, and your history — across sessions, across tools

**For AI assistants:**
- They stop forgetting everything between conversations
- They can understand not just your words but your intent, your mood, and your goals
- Multiple AI tools can share the same understanding of you, rather than each one starting from scratch

**For the bigger picture:**
- This is a shared language between humans and AI. Both can read it, both can write to it, and there's a built-in system to make sure neither side corrupts it
- It's an open standard — anyone can build tools that use it. No single company controls it
- As AI gets more capable, well-structured personal context becomes more valuable, not less. This is the foundation for AI that truly knows you and works for you

## What's Next

The standard is drafted. The three teams are collaborating. The next steps are to finalize the specification, build the first tools that create and read these knowledge units, and invite others to build on top of it.

It's early days, but the foundation is solid.

---

## Bibliography

**GitHub**
- UKU-Pebbles — https://github.com/m31uk3/uku-pebbles
- ai-pebbles (foundation project) — https://github.com/m31uk3/ai-pebbles
- SAGE (Sovereign Agent Governed Experience) — https://github.com/l33tdawg/sage

**X (Threads)**
- Convergence thread (Andy, l33tdawg, Luke) — https://x.com/kevinnguyendn/status/2035366573192753648
- Andy's OpenClaw PR announcement — https://x.com/kevinnguyendn/status/2035151222999851237
- Luke's UKU introduction — https://x.com/m31uk3/status/2035363053018272234
- Luke quoting Aaron Levie (Box CEO) on context — https://x.com/m31uk3/status/2035295106639802579
- Aaron Levie's original "context is king" post — https://x.com/levie/status/1962748473138401646
