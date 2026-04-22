# How to Create a Minimal, Reproducible Example (MRE)

**Source:** [Stack Overflow Help Center](https://stackoverflow.com/help/minimal-reproducible-example)
**Relevance:** The known-issue template's "Minimal Reproduction" section follows these principles.

---

When reporting an issue, provide enough context that someone else can reproduce the problem. This is called a "minimal, reproducible example" (MRE), also known as MCVE (minimal, complete, verifiable example) or reprex.

Your reproduction steps should be:

- **Minimal** — Use as few steps as possible that still trigger the issue
- **Complete** — Provide all parts someone needs to reproduce the problem
- **Reproducible** — Verify the steps actually trigger the issue before submitting

## Minimal

The more steps there are, the less likely someone can find the problem. Streamline:

1. **Restart from scratch.** Describe only what is needed to see the problem. Use simple, descriptive names.
2. **Divide and conquer.** If unsure of the source, start removing steps until the problem disappears — then add the last one back.

Keep it readable. Don't sacrifice clarity for brevity.

## Complete

All information necessary to reproduce the problem must be included:

- Include the environment (OS, tool version, config)
- If the problem spans multiple systems, include context for all of them
- Don't assume the reader has your local state

## Reproducible

Others need to verify the issue exists:

- **Describe the problem.** "It doesn't work" is not enough. State expected behavior vs actual behavior.
- **Eliminate irrelevant issues.** If the question isn't about a config error, make sure the config is valid.
- **Double-check that your steps reproduce the problem.** Test them in a fresh environment if possible.

## Application to Pebbles Known Issues

The `known-issue.user.json` template body includes:

```markdown
## Minimal Reproduction (MRE)

**Environment:**
**Steps:**
1.
2.
3.

**Expected:**
**Actual:**
```

This structure enforces MRE principles at capture time. The author must separate environment from steps, and expected from actual — preventing the "it doesn't work" anti-pattern.

## Further Reading

- Eric Lippert: [How to debug small programs](https://ericlippert.com/2014/03/05/how-to-debug-small-programs/)
- reprex (R): [Learn reprex](https://reprex.tidyverse.org/articles/learn-reprex.html)
