# Contributing to Sky Fetch Planner

## Development setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pip-audit
```

## Verification

```bash
python -m compileall -q src tests
ruff check src tests
pytest -q
pip-audit -r requirements.txt
docker build -t sky-fetch-planner .
docker run --rm --entrypoint=id sky-fetch-planner -u
```

## Scope and security

- Keep the component focused on validating and registering fetch plans; it does not execute network requests.
- Add tests for URL-policy and capacity changes.
- Do not add behavior intended to bypass authentication, robots/access controls, paywalls, or authorization boundaries.
- Any future network executor must independently validate resolved destinations and redirects and use network-layer egress controls.
- Keep product maturity claims aligned with verified implementation and CI evidence.

## Pull requests

1. Create a focused branch.
2. Make the smallest coherent change.
3. Run the verification commands above.
4. Document changes to URL/network security boundaries.
5. Open a pull request with a truthful maturity status.

## License

See `LICENSE`.
