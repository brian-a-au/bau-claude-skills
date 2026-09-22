# adobe-analytics-api-setup reference

Full detail behind the lean `SKILL.md`. This covers the Adobe Analytics API 2.0. For the CJA or AEP APIs, see the `adobe-cja-api-setup` skill.

## Scopes

Scopes define what the API client can do. Copy the exact scope string from the Developer Console credential.

| Purpose | Scopes |
|---------|--------|
| Minimum (verified) | `openid`, `AdobeID`, `additional_info.projectedProductContext` |
| Recommended for fuller coverage | add `read_organizations`, `additional_info.job_function` |

If your org's IMS rules require the recommended scopes for the endpoints `aa_auto_sdr` calls, you will see a `403` on `--list-reportsuites`, or empty `/dimensions` and `/metrics` responses, despite a successful auth. Add the recommended scopes to fix it.

## Product profile

Assign the OAuth integration to an Adobe Analytics product profile in the [Adobe Admin Console](https://adminconsole.adobe.com/):

1. Open the Admin Console.
2. Go to the Adobe Analytics product.
3. Select or create a product profile that has report suite access.
4. Add the service account (from the Developer Console project) to that profile.

Without this, authentication can succeed while no Analytics companies or report suites are visible. That is the most common reason `--list-reportsuites` returns nothing.

Note: this uses the Adobe Analytics Admin Console product, not Adobe Experience Platform. Do not add the AEP API for an Adobe Analytics setup.

## Error catalog

These generic OAuth errors are the same for any Adobe OAuth Server-to-Server credential:

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid_client` | Wrong or expired Client ID or Secret | Re-copy both from the console; check for stray spaces |
| `invalid_scope` | Scopes string was edited | Paste scopes exactly as shown |
| `unauthorized_client` | Not an OAuth Server-to-Server credential | Confirm the credential is OAuth Server-to-Server |
| `401 Unauthorized` | Expired token or regenerated credentials | Confirm the Org ID and current Secret |

**403, or empty report suite / dimension / metric results**, is the Adobe Analytics-specific case. Auth can succeed while the integration is not on an Adobe Analytics product profile, or a required scope is missing. Assign the Analytics product profile, add `read_organizations` and `additional_info.job_function`, and wait 5-10 minutes for the change to propagate.

## Security practices

- Never commit credentials. Gitignore `config.json`, `.env`, and any credential files.
- Inject secrets at runtime in CI/CD, and rotate the Client Secret periodically.
- Use a product profile with the minimum report suite access needed, and review API usage in the Developer Console.

## Key URLs

| Resource | URL |
|----------|-----|
| Adobe Developer Console | https://developer.adobe.com/console/ |
| Adobe Admin Console | https://adminconsole.adobe.com/ |
| Adobe Analytics 2.0 API docs | https://developer.adobe.com/analytics-apis/docs/2.0/ |

## Troubleshooting checklist

When authentication fails, verify:

- [ ] Organization ID ends with `@AdobeOrg`.
- [ ] Client ID copied exactly, no extra spaces.
- [ ] Client Secret is current (not regenerated since last copy).
- [ ] Scopes copied exactly, including the recommended ones if your org needs them.
- [ ] The Adobe Analytics API is in the project (not the AEP API).
- [ ] OAuth Server-to-Server is the selected auth type.
- [ ] The service account is on an Adobe Analytics product profile with report suite access.
- [ ] Waited 5-10 minutes after any permission change.
- [ ] `aa_auto_sdr --validate-config` and `--list-reportsuites` both work.
