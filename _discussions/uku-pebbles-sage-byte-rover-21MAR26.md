---
title: "Thread by @kevinnguyendn"
source: "https://x.com/kevinnguyendn/status/2035366573192753648"
author:
  - "[[@kevinnguyendn]]"
published: 2026-03-20
created: 2026-03-21
description:
tags:
  - "clippings"
---
**andy nguyen** @kevinnguyendn [2026-03-21](https://x.com/kevinnguyendn/status/2035151222999851237)

🚀 Huge architectural win for OpenClaw agents! Our PR #50848 just merged, officially passing the user's prompt into ContextEngine.assemble().

Why does this matter? It unlocks native selective retrieval for ByteRover. Instead of blindly prepending bloated memory files to every session, agents can now dynamically query their .brv/context-tree based on the exact user request.

✅ Cures agent amnesia

✅ Cuts token burn

✅ 100% backward compatible with legacy engines

Context that travels with the agent > context that dies with the session. 🧠⚡️

![[Clippings/z_attachments/2aa5874c34b0c644f873e296e4fef6f9_MD5.jpg]]

---

**l33tdawg** @l33tdawg [2026-03-21](https://x.com/l33tdawg/status/2035234434107293975)

Bro do try this

l33tdawg/sage: (S)AGE - (Sovereign) Agent Governed Experience
https://github.com/l33tdawg/sage

---

**andy nguyen** @kevinnguyendn [2026-03-21](https://x.com/kevinnguyendn/status/2035264670014357916)

This is insanely cool architecture. Just starred the repo! ⭐

We are actually completely aligned on the need for a consensus/validation layer for agent memory. Treating agent state like a distributed ledger to prevent "memory drift" is brilliant.

We're exploring some similar concepts for the validation layer in ByteRover. We are actually open-sourcing the CLI early next week, would absolutely love to get your eyes on it when it drops, and maybe even collaborate on some consensus ideas! 🤝

---

**Luke Jackson** @m31uk3 [2026-03-21](https://x.com/m31uk3/status/2035363053018272234)

This feels like perfect timing! 🔥

You’ve both built the runtime infrastructure for the schema spec I’ve been drafting all week.

What Pebbles Is

Pebbles is a format-independent schema spec for personal knowledge units enriched with rich experiential metadata captured at the moment of creation: intent, device/context, cognitive-emotional state, recall associations + interspecies caching signals.

YAML front-matter in Markdown is the v1 default binding (I call these UKUs — Universal Knowledge Units).

Related intro here: https://x.com/m31uk3/status/2035295106639802579…

This human-first layer feels like the exact missing piece that can feed directly into SAGE’s BFT validators/consensus engine and ByteRover’s context-tree retrieval (especially with the Obsidian curation you just mentioned). Gives agents structured, readable, sovereign memory that never drifts.

Super excited about the alignment. Would love to share the full spec + sample UKUs and explore how we can wire them together.

---

**andy nguyen** @kevinnguyendn [2026-03-21](https://x.com/kevinnguyendn/status/2035366573192753648)

Luke, this is incredible timing. We are all attacking the same "agent amnesia" problem from the three exact angles needed to solve it:

The Schema (Pebbles)
The Validation (SAGE)
The Retrieval/State (ByteRover)

YAML front-matter in Markdown is exactly how ByteRover structures its .brv/context-tree. I would absolutely love to see the Pebbles spec and explore wiring this up!

We are open-sourcing the ByteRover CLI early next week. Let's get a group chat going with @l33tdawg and actually build the standard for sovereign agent memory together. 🤝

---

**Luke Jackson** @m31uk3 [2026-03-21](https://x.com/m31uk3/status/2035366804495999338)

Let’s do it! 😎