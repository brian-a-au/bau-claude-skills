---
name: adobe-api-setup
description: Set up Adobe AEP/CJA API access with OAuth Server-to-Server auth. Use when configuring API credentials for the SDR tools or troubleshooting OAuth 401/403, invalid_client, or invalid_scope errors.
---

# Adobe AEP / CJA API Setup

Configure OAuth Server-to-Server credentials for Adobe Experience Platform (AEP) and Customer Journey Analytics (CJA) APIs. Use this when setting up credentials for the SDR tools (`aa_auto_sdr`, `cja_auto_sdr`, `sdr-grader`, `sdr-visualizer`) or when an API call returns an auth error.

## When to use

- Setting up API credentials for the first time.
- Wiring credentials into a project or CI pipeline.
- Diagnosing `401`, `403`, `invalid_client`, `invalid_scope`, or `unauthorized_client` errors.

## Prerequisites

Confirm the user has:

- Access to Adobe Experience Cloud with CJA and/or AEP.
- Access to the Adobe Developer Console with permission to create integrations.
- A System Administrator or Developer role (needed to create OAuth credentials).
- The right product profiles assigned in the Admin Console.

## Developer Console setup

1. Open the [Adobe Developer Console](https://developer.adobe.com/console/), sign in, and confirm the correct organization (top-right).
2. Create a new project with a descriptive name.
3. Add the **Customer Journey Analytics** API. Choose **OAuth Server-to-Server**. Select a product profile that can reach the target Data Views.
4. Add the **Experience Platform API** as well. Choose **OAuth Server-to-Server** and a product profile.

Both APIs share the same OAuth credentials.

> **Add the AEP API even for CJA-only work.** It associates the service account with an Experience Platform product profile, which CJA API authentication requires. Missing this is the most common cause of `403` errors.

## Credentials

Collect these four values from the OAuth Server-to-Server credential:

| Credential | Where | Example |
|------------|-------|---------|
| Organization ID | Project overview | `ABC123DEF456@AdobeOrg` |
| Client ID | Credential details | `cm1234567890abcdef...` |
| Client Secret | "Retrieve client secret" | `p8e-XXXX...` |
| Scopes | Credential scopes | space/comma-separated scope string |

Copy the scopes string exactly as shown. Editing it causes `invalid_scope`.

## Configuration methods

The SDR tools read credentials from environment variables, a `.env` file, or `config.json` (env vars take precedence). Field names are the same everywhere: `ORG_ID`, `CLIENT_ID`, `SECRET`, `SCOPES`.

```json
// config.json
{
  "org_id": "ABC123DEF456@AdobeOrg",
  "client_id": "YOUR_CLIENT_ID",
  "secret": "YOUR_CLIENT_SECRET",
  "scopes": "your_scopes_from_developer_console"
}
```

```bash
# environment variables
export ORG_ID="ABC123DEF456@AdobeOrg"
export CLIENT_ID="YOUR_CLIENT_ID"
export SECRET="YOUR_CLIENT_SECRET"
export SCOPES="openid,AdobeID,additional_info.projectedProductContext"
```

Never commit credentials. Add `config.json` and `.env` to `.gitignore`. Use a secrets store in CI.

## Top errors

| Error | Likely cause | Fix |
|-------|--------------|-----|
| `invalid_client` | Wrong/expired Client ID or Secret | Re-copy both from Developer Console; check for stray spaces |
| `invalid_scope` | Scopes string edited | Paste scopes exactly as shown |
| `unauthorized_client` | OAuth S2S not the selected auth type | Confirm the credential is OAuth Server-to-Server |
| `403 Forbidden` | Service account not on a required product profile, or AEP API missing | Add both CJA + AEP APIs; assign product profiles; wait 5-10 min |
| `401 Unauthorized` | Expired token or regenerated credentials | Confirm Org ID and current Secret |

For the full error catalog, product-profile detail, and a step-by-step troubleshooting checklist, see [reference.md](reference.md).
