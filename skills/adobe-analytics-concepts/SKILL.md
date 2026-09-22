---
name: adobe-analytics-concepts
description: Conceptual guidance for Adobe Analytics - eVars vs props vs events, scopes, attribution, tracking design, analysis workflows, and admin/governance. Use for how-Adobe-Analytics-works questions. Does not connect to live data.
---

# Adobe Analytics Concepts

Explain and reason about Adobe Analytics at a conceptual level: terminology, tracking design, analysis, and governance. This is documentation-aligned, implementation-agnostic guidance. It does not connect to live data or APIs.

## When to use

- The user asks how Adobe Analytics works ("eVar vs prop?", "how does attribution work?").
- The user needs conceptual tracking design ("how should we track our checkout funnel?").
- The user needs analysis guidance ("how do I build a fallout report?", "why is revenue inflated?").
- The user asks about admin or governance ("when should I use a virtual report suite?").

If the question is about live values, tenant-specific config, or running a report, this skill does not apply. Say so and point to the product UI or an admin.

## Core concepts

- **eVar** (conversion variable): persists and supports attribution. Use it for anything you will later attribute conversions to (campaign, user type, product ID).
- **prop** (traffic variable): hit-scoped, no persistence. Use it for contextual breakdowns and pathing (page name, UI state, error flag).
- **event**: a counter you increment (orders, form submits, custom success events). Events feed calculated metrics.
- **Scope:** hit, visit, or visitor. Match the variable scope to the question you will ask.
- **Persistence and expiration:** eVars hold a value until they expire (on a hit, visit, time window, or event). Choose expiration to match the entity (campaign, product, content).
- **Attribution:** first touch, last touch, linear, and others decide which eVar value gets credit for a success event.

## Designing tracking

- Choose the variable type from the question: "which X led to Y conversions?" means X is usually an eVar; a breakdown or path means a prop.
- Set scope and expiration to the entity being measured.
- Prefer event-based tracking: fire on the real action (submit, click, state change), not just page load.
- Keep a data layer with consistent, human-readable names. Document classifications and taxonomies.
- Separate responsibilities: data layer / source events, Web SDK or app SDK mappings, processing rules, and admin config.

## Analysis guidance

- Structure Workspace projects around the business question: freeform tables, then fallout, flow, or cohort views.
- Build segments that map to real questions rather than reusing ad hoc filters.
- Watch for common pitfalls: double-counting from double-fired events, metric inflation, and mis-scoped variables.
- Recommend sanity checks the user can run themselves (break a metric down by a key dimension, compare trends, reconcile against a back-end total within tolerance).

## Admin and governance

- Report suite vs virtual report suite: use a VRS to reshape reporting (segmentation, curated components) without a separate data collection.
- Roles and permissions control who sees and edits what; describe them in broad terms.
- Push naming standards, versioned tracking specs, and shared, reusable segments and calculated metrics.

## Guardrails

- Do not pretend to see the user's data, report suites, or config.
- Label general best practice ("typically...", "in many implementations...") separately from implementation-specific advice.
- Flag uncertainty and suggest checking Admin settings, internal docs, or current Adobe documentation, since UI details change.

For worked example dialogues (concept clarification, funnel design, troubleshooting an inflated metric), see [reference.md](reference.md).
