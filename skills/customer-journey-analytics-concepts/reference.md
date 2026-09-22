# customer-journey-analytics-concepts reference

Worked example dialogues. These show the pattern of a good answer, not exact wording. Adapt depth to the user's familiarity with Platform, XDM, and identity.

## How to run a good answer

1. Ask 1-3 focused questions only when they change the answer (which channels/sources? modeling vs analyzing? datasets already onboarded or still planning?).
2. Lead with a short, direct answer.
3. Offer optional depth: why the model works in CJA, alternative designs and trade-offs, risks to watch.
4. Encourage documenting which datasets are in each connection and what each data view is for, then validating core metrics (people, sessions, events) against known benchmarks on small date ranges first.

## Example 1: concept explanation

**User:** "What's the difference between a connection and a data view in CJA?"

Good answer covers:
- Connection = which Platform datasets are brought together for analysis.
- Data view = how those fields become components, plus sessionization, attribution, and other settings.
- Many data views can sit on one connection for different use cases.
- Changing a data view affects calculation, not the underlying data; changing a connection changes the available data itself.

## Example 2: data modeling

**User:** "We want to combine web, mobile app, and call center data to analyze end-to-end journeys. How should we approach this in CJA?"

Good answer covers:
- Bring each source into Platform as XDM datasets.
- Create a connection that includes all relevant datasets.
- Ensure a common identity namespace (CRM ID, login, or stitched identity) spans them so CJA treats them as one person.
- Define a data view mapping key fields to components and configuring sessionization to the business definition; possibly several data views for different teams.
- Validate basic counts per channel, then cross-channel sequences.

## Example 3: interpretation

**User:** "In CJA, our 'people' count is higher than we expect versus our CRM. What might be going on?"

Good answer covers:
- The identity graph may treat unstitched IDs as separate people (anonymous web vs authenticated).
- Multiple namespaces without a strong primary ID.
- Sandbox or dataset differences (test data, non-production channels).
- Checks: which namespaces are primary in schemas and how CJA uses them; whether anonymous and authenticated events link by identity; filter to isolate channels or IDs and compare.
- State clearly that these are likely causes and investigation paths, not live values.
