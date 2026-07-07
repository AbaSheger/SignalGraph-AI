# Incident Report: Auth Service JWT Validation Error

**Date:** 2024-04-01  
**Severity:** critical  
**Service:** auth-service  
**Error:** JWTValidationError  
**Status:** Resolved  

---

## Summary

The auth-service began rejecting all JWT tokens at 09:15 UTC, causing 100% authentication failure across all services that depend on it. The incident was classified as SEV-1. Total user-facing downtime was 23 minutes.

## Timeline

| Time (UTC) | Event |
|---|---|
| 09:15 | Spike in 401 Unauthorized responses detected |
| 09:18 | SEV-1 declared |
| 09:21 | Root cause identified: expired signing key |
| 09:38 | New signing key deployed and validated |

## Root cause

The JWT signing key used by auth-service had a 90-day expiry that was not tracked in any rotation schedule. The key expired silently at 09:15 UTC, causing all newly issued and validated tokens to fail with `JWTValidationError`.

## Fix

Rotate signing key by generating a new RSA-256 key pair, deploying the new public key to all dependent services (user-service, payment-api, order-service), and updating the auth-service secret store.

## Related services

- `auth-service` (primary affected)
- `user-service` (dependent, all auth flows broken)
- `payment-api` (downstream impact)

## Action items

- [ ] Add automated signing key rotation with 30-day advance warning
- [ ] Add key expiry monitoring to the SRE dashboard
- [ ] Document key rotation procedure in a dedicated runbook
