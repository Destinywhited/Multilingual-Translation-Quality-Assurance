# Recurring Error-Pattern Analysis

**Dataset:** Synthetic test cases

> These findings are illustrative. They do not establish real translation-engine performance or recurrence.

Total annotated errors: 6

## Counts by category

- accuracy: 4
- fluency: 1
- terminology: 1

## Annotated error patterns

### ES-002 — accuracy (critical)
- Language: ES
- Error span: `Administer this product`
- Description: The source prohibition is omitted, reversing the instruction.

### FR-002 — accuracy (critical)
- Language: FR
- Error span: `public`
- Description: The translation reverses the confidentiality requirement.

### DE-002 — accuracy (major)
- Language: DE
- Error span: `thirty months`
- Description: The translation changes the payment deadline from days to months.

### FR-003 — fluency (minor)
- Language: FR
- Error span: `Click on the button`
- Description: The wording is less concise than the preferred interface instruction.

### FR-004 — terminology (major)
- Language: FR
- Error span: `automatic saving`
- Description: The intended technical feature is automatic backup, not saving.

### DE-004 — accuracy (critical)
- Language: DE
- Error span: `renews automatically`
- Description: The translation omits the negation.

## Limitations

- No real machine-translation engine output was supplied.
- No engine identifiers or production corpus were supplied.
- The annotations are synthetic and manually authored.
- Repeated category counts alone do not prove a recurring engine-level failure.
