# Delta Macro Template

Use this file to document a single Delta macro from the client's COBOL macro library.
Save as `<engagement-name>/macros/<MACRO-NAME>.md` (filename in SCREAMING-SNAKE-CASE).

---

## Name

`DLTM-<MACRO-NAME>`

## Purpose

Describe what this macro does in plain English. What business operation does it perform?
What COBOL constructs does it expand to?

## Parameters

| Parameter | Type   | Description                        |
|-----------|--------|------------------------------------|
| PARAM-1   | TEXT   | Description of first parameter     |
| PARAM-2   | INT    | Description of second parameter    |

## Returns

Describe what the macro returns or what working storage fields it populates.

## Category

<category name>

## Example Usage

```cobol
CALL 'DLTM-<MACRO-NAME>' USING WS-PARAM-1, WS-PARAM-2.
```

## Notes

Any additional context, caveats, or deprecation warnings.
