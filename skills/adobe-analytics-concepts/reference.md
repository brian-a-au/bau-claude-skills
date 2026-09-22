# adobe-analytics-concepts reference

Worked example dialogues. These show the pattern of a good answer, not exact wording. Adjust depth to the user's expertise.

## How to run a good answer

1. Ask 1-3 focused questions only when they change the recommendation (web vs app? tracking vs interpreting? Web SDK vs older AppMeasurement/Launch?).
2. Lead with a 2-4 sentence direct answer.
3. Offer optional depth: why it works, alternatives and trade-offs, things to watch out for.
4. Encourage recording the decision in a tracking spec and validating in a debugger or a low-latency dev report suite.

## Example 1: concept clarification

**User:** "What's the difference between an eVar and a prop, and when should I use each?"

Good answer covers:
- eVar = conversion variable, persists, supports attribution.
- prop = traffic variable, hit-scoped, no persistence.
- Map to use cases: eVar for things you attribute conversions to (campaigns, user categories, product IDs); prop for contextual breakdowns and pathing (page names, UI states, error flags).
- Decision rule: "If someone will later ask 'which X led to Y conversions?', X usually belongs in an eVar."

## Example 2: implementation design

**User:** "We want to measure how many users complete a 4-step signup funnel. How should we design this?"

Good answer covers:
- Step signals: a step-name dimension (eVar) and/or a custom event per step.
- Event-based tracking: fire when each step actually completes (submit, click, state change).
- Analysis: a fallout-style view comparing step progression.
- Best practices: consistent step IDs/names, documented variable and event mappings, dev testing before rollout.

## Example 3: analysis troubleshooting

**User:** "Our 'Orders' metric looks inflated. What should we check?"

Good answer covers:
- Event firing logic (double firing on confirmation page load plus click).
- Order ID uniqueness (repeated IDs per visit).
- Segments that multiply counts (multiple hits per order).
- Sanity checks: break `Orders` down by `Order ID` to spot duplicates; reconcile a day's orders against the back-end total within tolerance.
- State clearly that these are troubleshooting steps, not live values.
