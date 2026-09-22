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

## Full error catalog

### invalid_client
```
{"error": "invalid_client", "error_description": "..."}
```
Causes: wrong Client ID, wrong or expired Secret, credentials regenerated.
Fixes: re-copy the Client ID exactly; re-retrieve the Secret; check for extra spaces.

### invalid_scope
```
{"error": "invalid_scope", "error_description": "..."}
```
Causes: the scopes string does not match the console; a requested scope is not authorized.
Fixes: copy scopes exactly from the credential; do not edit them.

### unauthorized_client
```
{"error": "unauthorized_client", "error_description": "..."}
```
Causes: OAuth Server-to-Server not enabled, or wrong credential configuration.
Fixes: confirm the credential is OAuth Server-to-Server.

### 403 or empty results
```
ERROR - 403 Forbidden
# or: --list-reportsuites returns nothing; /dimensions and /metrics are empty
```
Causes: the integration is not on an Adobe Analytics product profile, or a required scope is missing.
Fixes: assign the Analytics product profile; add `read_organizations` and `additional_info.job_function`; wait 5-10 minutes for changes to propagate.

### 401 Unauthorized
```
ERROR - 401 Unauthorized
```
Causes: expired or invalid token; credentials changed in the console.
Fixes: confirm credentials were not regenerated; confirm the Secret is current; confirm the Organization ID.

## Security practices

1. Never commit credentials. Gitignore `config.json`, `.env`, and any credential files.
2. Inject secrets at runtime in CI/CD.
3. Rotate the Client Secret periodically.
4. Use a product profile with the minimum report suite access needed.
5. Review API usage in the Developer Console.

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
