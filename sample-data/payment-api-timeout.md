# Incident Report: Payment API Timeout

**Date:** 2024-03-15  
**Severity:** high  
**Service:** payment-api  
**Error:** ConnectionTimeout  
**Status:** Resolved  

---

## Summary

The payment-api service experienced widespread connection timeouts starting at 14:32 UTC. Approximately 40% of payment processing requests failed with `ConnectionTimeout` errors. The incident lasted 47 minutes before full resolution.

## Timeline

| Time (UTC) | Event |
|---|---|
| 14:32 | First alerts triggered — p99 latency spike on payment-api |
| 14:35 | On-call engineer paged |
| 14:41 | Root cause identified: database connection pool exhaustion |
| 15:19 | Fix deployed and traffic normalised |

## Root cause

Upstream database connection pool exhaustion. The payment-api was configured with a maximum pool size of 10 connections. A traffic spike during a promotional campaign caused connection requests to queue and eventually time out after 5 seconds.

## Fix

Increased connection pool size from 10 to 50 and implemented a circuit breaker pattern to shed load gracefully when the pool is saturated.

## Related services

- `payment-api` (primary affected)
- `order-service` (downstream, degraded)

## Runbook

See `deployment-rollback-runbook.md` for rollback steps if the fix needs to be reverted.

## Action items

- [ ] Add autoscaling policy for connection pool based on request rate
- [ ] Improve connection pool exhaustion alerting with clearer runbook link
- [ ] Load test with 3× peak traffic before next promotional campaign
