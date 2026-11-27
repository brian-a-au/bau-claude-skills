# Standards

This folder holds the standards that the Adobe tooling repos share.

| File | What it is |
|---|---|
| [`adobe-credentials-v1.md`](adobe-credentials-v1.md) | The rules for how a tool finds, checks, shows and protects an Adobe credential |
| [`codes-v1.json`](codes-v1.json) | The codes for sign-in results, errors, notices and warnings |
| [`schemas/`](schemas/) | The JSON shapes for the config check, the live test and a tool's list of known differences |
| [`cases/adobe-credentials-v1/`](cases/adobe-credentials-v1/) | The shared test cases |
| [`cases/README.md`](cases/README.md) | The format of a case and how a tool runs the cases |
| [`sync_cases.py`](sync_cases.py) | Copies the cases, the shapes and the codes into a tool repo |

`scripts/validate_skills.py` checks these files in CI.
