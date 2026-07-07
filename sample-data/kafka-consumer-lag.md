# Incident Report: Kafka Consumer Lag

**Date:** 2024-04-18  
**Severity:** medium  
**Service:** event-processor  
**Error:** ConsumerLag  
**Status:** Resolved  

---

## Summary

The `event-processor` Kafka consumer group fell behind by over 500,000 messages starting at 22:00 UTC. The lag caused delayed event processing, leading to stale data in downstream dashboards and notifications. No data was lost.

## Timeline

| Time (UTC) | Event |
|---|---|
| 22:00 | Consumer lag alert triggered at 100k messages |
| 22:15 | On-call investigated — consumer CPU pegged at 100% |
| 22:40 | Consumer group scaled from 3 to 9 instances |
| 23:05 | Lag reduced to zero, processing caught up |

## Root cause

Under-provisioned consumer group. A 5× increase in event volume from a new client integration was not accounted for in capacity planning. The existing 3-consumer group could not keep pace, leading to growing `ConsumerLag`.

## Fix

Scale the consumer group from 3 to 9 instances using the Kubernetes HPA. Update the partition count on the topic from 3 to 9 to allow full parallelism.

## Related services

- `event-processor` (primary affected)
- `notification-service` (delayed notifications)
- `analytics-service` (stale metrics)

## Action items

- [ ] Add consumer lag auto-scaling policy
- [ ] Capacity plan for new client integrations before go-live
- [ ] Set consumer lag SLO at 10,000 messages with paging alert
