# Changelog

## 0.1.0 — Engineering beta

- replace misleading in-memory `queued` scraper behavior with a truthful fetch-plan registry
- require HTTPS and reject embedded credentials, localhost, and non-global IP literals
- add optional hostname allowlist via `SKY_FETCH_ALLOW_HOSTS`
- bound selector length and in-memory plan capacity
- add plan IDs, retrieval, health/readiness endpoints, and tests
- replace fake Node build/test scripts with Python compile, Ruff, pytest and dependency-audit gates
- add non-root container packaging and runtime health smoke verification
- document planning/execution separation and SSRF/access-control boundaries

No network fetching, crawler execution, durable scheduling, HA, or production deployment is claimed.
