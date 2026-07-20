---
name: slugify
description: Convert a phrase, title, or filename into a kebab-case URL slug. Use whenever the user asks to slugify text, make a slug, or turn a title into a URL-safe identifier.
---

# slugify

Turn the given text into a **kebab-case slug**:

- lowercase everything
- keep only ASCII letters and digits; every other run of characters (spaces,
  punctuation, symbols) becomes a single hyphen
- no leading or trailing hyphens, no doubled hyphens

Examples:

- `Hello, World! 2024` → `hello-world-2024`
- `Report_v2 (final)` → `report-v2-final`
- `  spaced   out  ` → `spaced-out`

Respond with **only the slug**, on its own line — no quotes, no explanation.
