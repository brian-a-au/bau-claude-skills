---
name: adobe-analytics-api-setup
description: Set up Adobe Analytics API 2.0 access with OAuth Server-to-Server auth. Use when configuring credentials for aa_auto_sdr or other Adobe Analytics report-suite integrations, or troubleshooting OAuth 401/403, invalid_client, invalid_scope, or empty report-suite/dimension/metric results. For CJA or AEP, use adobe-cja-api-setup instead.
---

# Adobe Analytics API 2.0 Setup

Configure OAuth Server-to-Server credentials for the Adobe Analytics API 2.0. Use this for `aa_auto_sdr` and other Adobe Analytics report-suite integrations.

This is different from the CJA setup. Adobe Analytics needs the Adobe Analytics API and an Adobe Analytics product profile, and it does not need the AEP API. For CJA or AEP, use the `adobe-cja-api-setup` skill.

## When to use

- Setting up credentials for `aa_auto_sdr` or another Adobe Analytics API 2.0 integration.
- Diagnosing `401`, `403`, `invalid_client`, or `invalid_scope` errors on an Adobe Analytics API call.
- Auth appears to succeed but `--list-reportsuites` returns nothing, or `/dimensions` and `/metrics` come back empty. This usually means a missing product profile or a missing recommended scope.

## Prerequisites

Confirm the user has:

- Access to Adobe Analytics with the report suites they want to document.
- Access to the Adobe Developer Console with permission to create integrations.
- A System Administrator or Developer role (needed to create OAuth credentials).
- Adobe Analytics admin access to assign the integration to a product profile.

## Developer Console setup

1. Open the [Adobe Developer Console](https://developer.adobe.com/console/), sign in, and confirm the correct organization (top-right).
2. Create a new project with a descriptive name.
3. Add the **Adobe Analytics API**. Choose **OAuth Server-to-Server**. Use the default version the console offers.

You do not add the Experience Platform API. That is only for CJA and AEP.

## Product profile

In the [Adobe Admin Console](https://adminconsole.adobe.com/), add your OAuth integration to an **Adobe Analytics product profile**. This step is critical. Without it, authentication can succeed while no Analytics companies or report suites are visible, so `aa_auto_sdr --list-reportsuites` returns nothing.

## Credentials

Collect these four values from the OAuth Server-to-Server credential:

| Credential | Where | Example |
|------------|-------|---------|
| Organization ID | Project overview | `ABC123DEF456@AdobeOrg` |
| Client ID | Credential details | `cm1234567890abcdef...` |
| Client Secret | "Retrieve client secret" | `p8e-XXXX...` |
| Scopes | Credential scopes | comma-separated scope string |

## Scopes

The `SCOPES` value must include these three at a minimum:

```
openid
AdobeID
additional_info.projectedProductContext
```

Two more are recommended for fuller endpoint coverage:

```
read_organizations
additional_info.job_function
```

If your org's IMS rules require the recommended scopes for the endpoints this tool calls, you will see a `403` on `--list-reportsuites`, or empty `/dimensions` and `/metrics` responses, even though auth succeeded. Add the recommended scopes when that happens.

## Configuration methods

`aa_auto_sdr` resolves credentials in this order: `--profile` first, then environment variables, then a `.env` file, then `config.json`. Field names are the same everywhere: `ORG_ID`, `CLIENT_ID`, `SECRET`, `SCOPES`.

```json
// config.json
{
  "org_id": "ABC123DEF456@AdobeOrg",
  "client_id": "YOUR_CLIENT_ID",
  "secret": "YOUR_CLIENT_SECRET",
  "scopes": "openid,AdobeID,read_organizations,additional_info.projectedProductContext,additional_info.job_function"
}
```

```bash
# environment variables
export ORG_ID="ABC123DEF456@AdobeOrg"
export CLIENT_ID="YOUR_CLIENT_ID"
export SECRET="YOUR_CLIENT_SECRET"
export SCOPES="openid,AdobeID,read_organizations,additional_info.projectedProductContext,additional_info.job_function"
```

For named profiles, `aa_auto_sdr --profile-add NAME` captures these interactively into `~/.aa/orgs/NAME/config.json`. Never commit credentials. Add `config.json` and `.env` to `.gitignore`. Use a secrets store in CI.

## Top errors

| Error | Likely cause | Fix |
|-------|--------------|-----|
| `invalid_client` | Wrong/expired Client ID or Secret | Re-copy both from Developer Console; check for stray spaces |
| `invalid_scope` | Scopes string edited | Paste scopes exactly as shown |
| `unauthorized_client` | OAuth S2S not the selected auth type | Confirm the credential is OAuth Server-to-Server |
| `403` or empty report suites/dimensions/metrics | Integration not on an Adobe Analytics product profile, or a recommended scope missing | Assign the Analytics product profile; add `read_organizations` and `additional_info.job_function`; wait 5-10 min |
| `401 Unauthorized` | Expired token or regenerated credentials | Confirm Org ID and current Secret |

Verify with `aa_auto_sdr --validate-config` and `aa_auto_sdr --list-reportsuites`. For the full error catalog and a troubleshooting checklist, see [reference.md](reference.md).
