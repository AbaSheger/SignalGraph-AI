# Runbook: Deployment Rollback

**Type:** runbook  
**Owner:** Platform Engineering  
**Last Updated:** 2024-03-01  

---

## Overview

This runbook describes the procedure for rolling back a deployment when a release introduces regressions or outages. It covers rollback criteria, step-by-step instructions, verification and post-rollback actions.

---

## Rollback Criteria

Initiate a rollback if any of the following are true:

- Error rate on the affected service exceeds 5% for more than 3 minutes
- P99 latency exceeds 2× the pre-deployment baseline
- A SEV-1 or SEV-2 incident has been declared related to the deployment

---

## Rollback Steps

### 1. Identify the previous stable image

```bash
kubectl rollout history deployment/<service-name> -n production
```

### 2. Trigger rollback

```bash
kubectl rollout undo deployment/<service-name> -n production
```

### 3. Monitor rollout progress

```bash
kubectl rollout status deployment/<service-name> -n production --watch
```

### 4. Verify traffic is recovering

Check the service dashboard for error rate and latency returning to baseline. Allow 5 minutes for full traffic normalization.

---

## Post-Rollback Checks

- Confirm all health checks are passing
- Notify the incident channel that rollback is complete
- Open a post-rollback review ticket with the root cause of the failed deployment
- Freeze further deployments to the service until the root cause is fixed

---

## Related Services

If rolling back a shared library or platform service, check for downstream impact on dependent services:
- Trigger smoke tests for each downstream service
- Check inter-service health dashboards

---

## Escalation

If rollback does not restore service within 15 minutes, escalate to the on-call engineering manager and initiate a war room.
