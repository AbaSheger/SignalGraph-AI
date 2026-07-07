# Postmortem: Multi-Service Outage — Payment & Auth (2024-04-02)

**Date:** 2024-04-02  
**Severity:** critical  
**Status:** Resolved  
**Duration:** 1 hour 12 minutes  
**Services Affected:** payment-api, auth-service, user-service, order-service  

---

## Executive Summary

On 2024-04-02, a sequence of failures originating in `auth-service` caused a cascading outage affecting `payment-api` and downstream services. The root cause was an expired JWT signing key that invalidated all active sessions, combined with an inadequate circuit breaker configuration that allowed the failure to propagate rather than gracefully degrade.

---

## Timeline

| Time (UTC) | Event |
|---|---|
| 09:15 | `auth-service` JWT signing key expired — all new token validations fail |
| 09:17 | `payment-api` begins returning 401 errors — circuit breaker not triggered |
| 09:18 | SEV-1 declared |
| 09:21 | Root cause identified in auth-service |
| 09:38 | New signing key deployed to auth-service |
| 09:45 | payment-api circuit breaker reset; traffic recovering |
| 10:27 | All services confirmed healthy |

---

## Contributing Factors

1. **No key rotation schedule** — The JWT signing key had a 90-day TTL with no automated rotation or advance alerting.
2. **Missing circuit breaker on payment-api** — The payment-api did not have a circuit breaker for auth failures, so it continued attempting auth checks and propagating errors to users.
3. **Insufficient monitoring** — No alert was configured for auth-service error rate crossing 10%.

---

## Root Cause

The JWT signing key used by `auth-service` expired silently at 09:15 UTC. Because no rotation schedule existed and no expiry monitoring was in place, the expiry was not detected until user-facing errors appeared.

## Fix

- Rotated the JWT signing key (emergency fix)
- Added circuit breaker to payment-api for auth dependencies
- Added key expiry monitoring alert (fires 7 days before expiry)

---

## Action Items

| Item | Owner | Due |
|---|---|---|
| Implement automated key rotation | Auth Team | 2024-04-15 |
| Add auth error rate alerting | SRE | 2024-04-10 |
| Add circuit breaker to payment-api for all auth calls | Payment Team | 2024-04-12 |
| Write JWT key rotation runbook | Auth Team | 2024-04-20 |

---

## Lessons Learned

- Credentials and keys with TTLs must be tracked in a rotation schedule with automated alerting.
- Circuit breakers should be applied to all cross-service dependencies, especially auth.
- Postmortems should be scheduled within 48 hours of SEV-1 resolution.
