# Runbook: PostgreSQL Connection Pool Management

**Type:** runbook  
**Owner:** Platform Engineering  
**Last Updated:** 2024-03-20  

---

## Overview

This runbook covers diagnosis, tuning and emergency procedures for PostgreSQL connection pool issues. Connection pool exhaustion is a leading cause of service timeouts in the platform.

---

## Diagnosis Steps

### 1. Check active connections

```sql
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
SELECT count(*) FROM pg_stat_activity WHERE wait_event_type = 'Lock';
```

### 2. Identify connection-heavy services

```sql
SELECT application_name, count(*) 
FROM pg_stat_activity 
GROUP BY application_name 
ORDER BY count DESC;
```

### 3. Check pool configuration

For each service, inspect the `DATABASE_POOL_SIZE` and `DATABASE_MAX_OVERFLOW` environment variables.

---

## Tuning Parameters

| Parameter | Default | Recommended |
|---|---|---|
| pool_size | 10 | 20–50 |
| max_overflow | 10 | 10–20 |
| pool_timeout | 30s | 10s |
| pool_recycle | 3600s | 1800s |

---

## Emergency Procedures

### Kill idle connections

```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
  AND state_change < NOW() - INTERVAL '10 minutes';
```

### Increase pool size temporarily

Update the `DATABASE_POOL_SIZE` environment variable and restart the affected service.

---

## Prevention

- Set connection pool size based on load tests (2× expected peak)
- Enable connection pool metrics in Prometheus
- Add alerting on `pg_stat_activity` count > 80% of `max_connections`
