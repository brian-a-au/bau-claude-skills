# adobe-cja-api-setup reference

Full detail behind the lean `SKILL.md`: complete error catalog, product-profile requirements, scopes, and a troubleshooting checklist. This covers the CJA and AEP APIs. For the Adobe Analytics API 2.0, see the `adobe-analytics-api-setup` skill.

## OAuth scopes

Scopes define what the API client can do. Copy the exact scope string from the Developer Console credential.

| API | Typical scopes |
|-----|----------------|
| CJA read | `openid, AdobeID, read_organizations, additional_info.projectedProductContext` |
| CJA + AEP | The above plus the AEP scopes shown in your project |

Broader org access sometimes needs `read_organizations` and `additional_info.job_function`. Do not invent scopes; use what the console shows.

## Product profiles

### CJA

| Profile type | Grants |
|--------------|--------|
| Data View access | Read access to specific Data Views |
| Component access | Metrics, dimensions, segments, calculated metrics |
| Admin | Full access including configuration |

### AEP

Even for CJA-only projects, the service account needs an AEP product profile:

1. Open the [Adobe Admin Console](https://adminconsole.adobe.com/).
2. Go to **Products > Adobe Experience Platform**.
3. Select or create a product profile.
4. Assign the service account from the Developer Console project.

## Full error catalog

### invalid_client
```
{"error": "invalid_client", "error_description": "..."}
```
Causes: wrong Client ID, wrong or expired Secret, credentials regenerated.
Fixes: re-copy the Client ID exactly; re-retrieve the Secret; check for extra spaces or missing characters.

### invalid_scope
```
{"error": "invalid_scope", "error_description": "..."}
```
Causes: the scopes string does not match the console; a requested scope is not authorized.
Fixes: copy scopes exactly from the credential; do not add or edit them.

### unauthorized_client
```
{"error": "unauthorized_client", "error_description": "..."}
```
Causes: OAuth Server-to-Server not enabled, or wrong credential configuration.
Fixes: confirm the credential is OAuth Server-to-Server.

### 403 Forbidden
```
ERROR - 403 Forbidden
ERROR - Failed to fetch data: 403
```
Causes: service account not on the required product profiles; AEP API missing from the project; insufficient permission for the resource.
Fixes: confirm both CJA API and AEP API are in the project; check product-profile assignments; wait 5-10 minutes for permission changes to propagate.

### 401 Unauthorized
```
ERROR - 401 Unauthorized
ERROR - Authentication failed
```
Causes: expired or invalid token; credentials changed in the console.
Fixes: confirm credentials were not regenerated; confirm the Secret is current; confirm the Organization ID.

## Security practices

1. Never commit credentials. Gitignore `config.json`, `.env`, and any credential files.
2. Inject secrets at runtime in CI/CD.
3. Rotate the Client Secret periodically.
4. Use product profiles with the minimum permissions needed.
5. Review API usage in the Developer Console.

Suggested `.gitignore` entries:
```gitignore
config.json
.env
*.secret
.cja/
credentials/
```

## Key URLs

| Resource | URL |
|----------|-----|
| Adobe Developer Console | https://developer.adobe.com/console/ |
| Adobe Admin Console | https://adminconsole.adobe.com/ |
| CJA API docs | https://developer.adobe.com/cja-apis/docs/ |
| AEP API docs | https://developer.adobe.com/experience-platform-apis/ |

## Troubleshooting checklist

When authentication fails, verify:

- [ ] Organization ID ends with `@AdobeOrg`.
- [ ] Client ID copied exactly, no extra spaces.
- [ ] Client Secret is current (not regenerated since last copy).
- [ ] Scopes copied exactly from the console.
- [ ] Both CJA API and AEP API are in the project.
- [ ] OAuth Server-to-Server is the selected auth type.
- [ ] Service account is assigned to the product profiles.
- [ ] Product profiles have the needed permissions.
- [ ] Waited 5-10 minutes after any permission change.
