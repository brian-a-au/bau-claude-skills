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

## Error catalog

These generic OAuth errors are the same for any Adobe OAuth Server-to-Server credential:

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid_client` | Wrong or expired Client ID or Secret | Re-copy both from the console; check for stray spaces |
| `invalid_scope` | Scopes string was edited | Paste scopes exactly as shown |
| `unauthorized_client` | Not an OAuth Server-to-Server credential | Confirm the credential is OAuth Server-to-Server |
| `401 Unauthorized` | Expired token or regenerated credentials | Confirm the Org ID and current Secret |

**403 Forbidden** is the CJA-specific case. It usually means the service account is not on the required product profiles, or the AEP API is missing from the project. Confirm both the CJA API and the AEP API are in the project, check the product-profile assignments, and wait 5-10 minutes for the change to propagate.

## Security practices

- Never commit credentials. Gitignore `config.json`, `.env`, and any credential files.
- Inject secrets at runtime in CI/CD, and rotate the Client Secret periodically.
- Use product profiles with the minimum permissions needed, and review API usage in the Developer Console.

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
