# Domain — add a new domain

The playbook for adding a business area to the graph. **Base requirement:** the root
`LYNK.md` already exists and we know the business — if not, run `references/init.md` first.

Share the plan first, then update the user step by step as a todo list.

## 1. Create the domain folder

`domains/<name>/` — lowercase, underscores.

## 2. Write the domain's `LYNK.md`

The domain's context file. Ask guiding questions and write down:

- What is this domain about?
- What is its role and its goals?
- Who are its users, and what are they trying to do?

Keep it short and concrete — this is what future sessions ground on when working in this
domain.

## 3. Glossary deltas

Ask: **are there glossary terms that mean something different in this domain vs. the core
domain?** (e.g. "revenue" in finance vs. marketing). If yes, capture them in the domain's
`GLOSSARY.yml` — only the terms that differ, never a copy of the core glossary. If none,
move on.

## 4. Import entities from core

Ask **which core entities this domain needs**, and whether they want **special changes that
are only relevant to this domain** (domain-specific features, metrics, or descriptions).
Import each chosen entity by extending it from core (identity pointing at the core entity,
cherry-picking what's needed) — per the docs' extending mechanism.

## 5. New entities?

Ask if they want to add an entity that's **new** to this domain (not in core). If yes, follow
`references/entity.md` for each.

Done: the domain has context, its vocabulary deltas, the core entities it needs, and any new
ones. Suggest validating what you built.
