# topic_index.md - ThingsBoard CE Knowledge Entry

Objetivo: reduzir tokens iniciando por trilhas curtas e operacionais.

## authentication
- Start: `runbooks/rest-api-auth.md`.
- Then: curated `api/` reference when runbook is not enough.
- Fallback: upstream official docs only for unresolved auth edge cases.

## devices
- Start: `runbooks/create-device.md` and `runbooks/check-device-token.md`.
- Then: curated `user-guide/` notes for entity model details.
- Fallback: upstream official docs for advanced provisioning.

## telemetry
- Start: `runbooks/send-http-telemetry.md`.
- Then: curated `api/` payload and endpoint details.
- Fallback: upstream official docs for protocol variants.

## attributes
- Start: `runbooks/validate-attributes.md`.
- Then: curated `api/` and `user-guide/` references.
- Fallback: upstream official docs for advanced attribute scopes.

## dashboards
- Start: `runbooks/basic-dashboard-check.md`.
- Then: curated `user-guide/` dashboard patterns.
- Fallback: upstream official docs for widget-level deep dives.

## rule-engine
- Start: `runbooks/rule-engine-first-check.md`.
- Then: curated `user-guide/` rule chain notes.
- Fallback: upstream official docs for advanced rule nodes.

## rest-api
- Start: `runbooks/rest-api-auth.md`.
- Then: curated `api/` endpoints and examples.
- Fallback: upstream official docs for endpoint coverage gaps.

## troubleshooting
- Start: `runbooks/troubleshooting-ingestion.md`.
- For offline station or red dashboard state: `runbooks/station-offline-triage.md`.
- Then: other runbooks linked in error context.
- Fallback: curated `reference/` and upstream official docs if needed.

## unknown-or-unclear
- Start: `reading_priority.md`.
- Then: locate the nearest operational theme in this order: `rest-api`, `devices`, `telemetry`, `attributes`, `dashboards`, `rule-engine`, `troubleshooting`.
- Then: search local curated docs in `api/`, `user-guide/` and `tutorials/`.
- Fallback: upstream official docs only after exhausting the local KB.

## retrieval-policy
- Goal: minimum token consumption with maximum operational precision.
- Preferred source order: `topic_index.md` -> runbook -> local curated docs -> upstream official docs.
- If execution intent is unclear, search this KB first instead of guessing.
