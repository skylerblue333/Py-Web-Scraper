# Security Policy

## Supported status

Sky Fetch Planner is an **engineering beta**. CI verifies compilation, linting, tests, dependency audit, container build, non-root execution, and a liveness smoke check. These checks do not establish production security or deployment readiness.

## Current boundaries

The planner accepts HTTPS URLs only, rejects embedded credentials, localhost, and non-global IP literals, and can require an explicit hostname allowlist. It performs no network request and therefore does not claim complete SSRF protection for a future executor.

Any future fetch worker must re-resolve and validate network destinations at connection time, control redirects, use egress/network policy, apply request-size/time limits, and respect applicable access restrictions. Do not use the planner to bypass authentication, robots/access controls, paywalls, or authorization boundaries.

## Reporting

Report suspected vulnerabilities privately through GitHub security reporting when available. Do not include credentials, private target URLs, or sensitive fetched content in public issues.
