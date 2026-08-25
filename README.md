# Sky Fetch Planner — Python Engineering Beta

Sky Fetch Planner is a small FastAPI service for validating and registering bounded web-fetch plans. It is intentionally a **planning and policy component**, not a crawler executor.

## Status

**Engineering beta.** The service accepts HTTPS targets, rejects embedded credentials, localhost, and non-global IP literals, optionally enforces a hostname allowlist, caps selector and in-memory plan sizes, and provides health/readiness endpoints, tests, dependency auditing, and non-root container verification.

It does **not** perform network requests, execute JavaScript, bypass robots/access controls, store scraped content, or claim distributed crawling, durable scheduling, HA, or production deployment.

## API

- `GET /healthz` — process liveness.
- `GET /readyz` — reports in-memory planning capacity.
- `POST /v1/plans` — validate and register `{ "url": "https://example.com/docs", "selector": "main h1" }`.
- `GET /v1/plans/{id}` — retrieve a registered plan.

Set `SKY_FETCH_ALLOW_HOSTS=docs.example.com,status.example.com` to restrict accepted plans to an explicit hostname set. An empty value allows any hostname that passes the local URL policy; this still does not trigger a network request.

## Run locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 127.0.0.1 --port 8000
```

## Verify

```bash
pip install pip-audit
python -m compileall -q src tests
ruff check src tests
pytest -q
pip-audit -r requirements.txt
docker build -t sky-fetch-planner .
docker run --rm --entrypoint=id sky-fetch-planner -u
```

The container is expected to run as UID `10001`. CI also starts the container and verifies `/healthz`.

## Architecture

`src/main.py` is the canonical service. Plans are held in a bounded in-memory `OrderedDict` and disappear when the process exits. URL validation is a planning-time policy only. If a future executor is added, it must perform fresh DNS/IP checks at connection time, enforce redirect policy, respect applicable site access rules, and use network-layer egress controls rather than assuming this planner alone prevents SSRF.

## SKYCOIN4444 integration

Ecosystem services can use this component to validate and persist short-lived fetch intentions before handing approved plans to a separate controlled worker. Keeping planning and execution separate provides a stable interface without implying unrestricted scraping capability.

## Security and operational boundaries

The planner does not authenticate callers, provide tenant isolation, rate-limit requests, resolve DNS, verify redirects, enforce robots.txt, execute fetches, or provide durable storage. Do not treat planning-time URL checks as a complete SSRF defense for a future network executor.

## License

See `LICENSE`.
