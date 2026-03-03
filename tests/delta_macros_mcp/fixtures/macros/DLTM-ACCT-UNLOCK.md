## Name

`DLTM-ACCT-UNLOCK`

## Purpose

Unlocks a previously locked customer account and restores normal transaction access.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| ACCT-ID | TEXT | The account identifier to unlock |

## Returns

Sets WS-ACCT-LOCK-STATUS to ACTIVE on success or ERROR-UNLOCK on failure.

## Category

Account Management

## Example Usage

```cobol
CALL 'DLTM-ACCT-UNLOCK' USING WS-ACCT-ID.
```

## Notes

Caller must verify account is in LOCKED state before invoking.
