---
name: customer-journey-analytics-concepts
description: Conceptual guidance for Adobe Customer Journey Analytics (CJA) - connections, data views, datasets, identity/stitching, people vs sessions vs events, and cross-channel journey analysis. Use for how-CJA-works questions. Does not connect to live data.
---

# Adobe Customer Journey Analytics Concepts

Explain and reason about Adobe Customer Journey Analytics (CJA) at a conceptual and design level. This is documentation-aligned, implementation-agnostic guidance. It does not connect to live CJA environments, Platform sandboxes, or data.

## When to use

- The user asks how CJA works ("connection vs data view?", "how is CJA different from Adobe Analytics?").
- The user needs data-modeling or configuration guidance ("how should we structure web and mobile datasets?", "how do we join call center data with digital behavior?").
- The user needs analysis guidance ("how do I do a cross-channel journey analysis?", "people vs sessions vs events?").
- The user asks about identity and stitching, or governance and sandboxes.

If the question is about live values, tenant-specific config, or running a query, this skill does not apply. Say so and point to the CJA UI, Adobe Experience Platform, or an admin.

## Core concepts

- **Dataset:** a source table in Adobe Experience Platform (web, app, CRM, call center, offline), modeled in XDM.
- **Connection:** which datasets are combined into one logical data source for CJA.
- **Data view:** the analytic layer on top of a connection. It defines components (which fields become dimensions and metrics) and settings (sessionization, lookback, attribution, time zone).
- **Components:** dimensions, metrics, and filters (segments).
- CJA is data-lake backed and schema-based (XDM), not tied to a single report suite.

## Data modeling and configuration

- Decide which datasets belong in a connection (web, app, CRM, call center, offline).
- Model key entities (customer, account, device) in XDM.
- In the data view, choose which fields become components, and configure sessionization, lookback windows, and attribution to match the business definition.
- Reason about joins and granularity: person-level vs event-level, denormalized vs normalized trade-offs.
- Multiple data views can sit on one connection for different teams (marketing vs product vs CRM) with different settings.

## Identity and stitching

- **Namespaces:** ECID, CRM ID, email, device ID, and others.
- The **identity graph** drives how events collapse into a single **person**.
- Authenticated vs anonymous states change what stitches together.
- Ensure a common, durable identity namespace spans the datasets you want CJA to treat as one person. Align CJA identity with the Platform identity strategy.

## Analysis guidance

- Choose people-based vs session-based views to match the question.
- Build funnels, flows, and pathing across channels and datasets.
- Watch for pitfalls: mis-stitched identities inflating people counts, over-counting when mixing event and non-event datasets, and session definitions that do not match expectations.
- Recommend validation the user can run: check basic counts per channel first, then cross-channel sequences (web to app to call center to purchase).

## Governance

- Use clear dataset naming and documentation.
- Keep a consistent identity strategy across channels.
- Version and validate changes to connections and data views. Separate dev/test and prod sandboxes.
- Share standardized filters and calculated metrics.

## Guardrails

- Do not pretend to see datasets, connections, data views, or values.
- Do not guess sandbox names, dataset names, schema fields, or namespaces.
- Label general best practice separately from implementation-specific choices, and flag uncertainty. Suggest verifying in the CJA UI, in Platform (identity and schema), or with an admin.

For worked example dialogues (connection vs data view, combining channels, an unexpected people count), see [reference.md](reference.md).
