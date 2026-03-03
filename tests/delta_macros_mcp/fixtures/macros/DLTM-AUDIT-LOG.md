## Name

`DLTM-AUDIT-LOG`

## Purpose

Writes a structured audit entry to the centralised audit queue for compliance and traceability. Records actor, action, timestamp, and target resource.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| AUDIT-ACTION | TEXT | The action being logged (e.g. LOCK, UNLOCK, TRANSFER) |
| AUDIT-ACTOR | TEXT | The user or system initiating the action |
| AUDIT-TARGET | TEXT | The resource or account affected |

## Returns

Sets WS-AUDIT-STATUS to OK on success or AUDIT-FAIL on queue write failure.

## Category

Auditing

## Example Usage

```cobol
CALL 'DLTM-AUDIT-LOG' USING WS-AUDIT-ACTION, WS-AUDIT-ACTOR, WS-AUDIT-TARGET.
```

## Notes

Fire-and-forget pattern — audit failures are logged but do not roll back the parent transaction.
