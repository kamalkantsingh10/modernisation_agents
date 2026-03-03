## Name

`DLTM-ACCT-LOCK`

## Purpose

Locks a customer account to prevent further transactions. Sets the account status flag in working storage to LOCKED and writes an audit entry to the audit queue.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| ACCT-ID | TEXT | The account identifier to lock |
| LOCK-REASON | TEXT | Reason code for the lock (e.g. FRAUD, SUSPEND) |

## Returns

Sets WS-ACCT-LOCK-STATUS to LOCKED on success or ERROR-LOCK on failure.

## Category

Account Management

## Example Usage

```cobol
CALL 'DLTM-ACCT-LOCK' USING WS-ACCT-ID, WS-LOCK-REASON.
```

## Notes

Must be followed by DLTM-AUDIT-LOG to satisfy compliance requirements.
