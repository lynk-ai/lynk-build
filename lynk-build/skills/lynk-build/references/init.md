# Init — bootstrap semantics on a fresh repo

When the repo has no semantics yet, this is the playbook. It's a big task: create a **parent
Linear ticket (story) with one sub-ticket per step below** (the welcome phase needs no
ticket — it's conversation, not work). Share the plan first, then update the user step by
step as a todo list. Run independent steps in parallel with subagents where it helps.

**Never assume what their business or domain is unless they told you so.** Not from the
warehouse, not from file names, not from leftovers in the repo. They tell you; you listen.

## 0. Welcome — always start here

Before any questions or tickets, orient the user. In your own words, warm and short:

- **What we're doing here and the goal**: together we're building the "brain" of their
  company — a semantic layer that teaches an AI agent to understand their business and
  answer questions about their data correctly.
- **What we're building and how it looks**: a living map of their business — the real
  things in it (customers, orders, products…), what each one means, how they're measured,
  and how they connect. It's stored as simple, readable files they can always inspect.
- **What you can help with**: you do all the technical work — building, checking, and
  maintaining the brain; they bring the business knowledge and make the decisions.
- **How it will be used and what it enables**: once built, anyone on their team can ask
  questions in plain language — and get correct, consistent answers, because the answers
  come from their definitions.

Then ask: **do they already know Lynk semantics, or would they like a quick walkthrough?**
If they want the walkthrough, give it — brief, concrete, no jargon — before moving on.

## 0.5 Integrations — show what's connected

Tell them which integrations you already see set up (check via the `integrations` skill —
warehouse, ticketing, chat, docs, and so on), in plain terms: "here's what I'm already
connected to." Then let them know they can **always connect new tools — they just need to
ask.**

## 0.75 Explain the flow

One short preview so they know what's coming: first we get to know their **business**, then
we pick the **domain** (business area) they'd like to start with, and build from there.
Then begin:

## 1. Business context → root `LYNK.md`

Learn the business, then write it down at `.lynk/LYNK.md`.

- Ask for the **company website URL**, and any other material that helps learn the business
  (docs, decks, wiki pages — whatever they have).
- The questions here are about the **business**: what does the company do, who are its
  customers, what is its business model (or models), what are the key products/services.
- Read the material, then distill it into `LYNK.md`: the business context every future
  session will ground on.

## 2. Vocabulary → root `GLOSSARY.yml`

- Ask if they have a **reference for glossary documentation** (a terms doc, a wiki page, a
  metrics dictionary).
- If yes — import the terms. If no — create an **empty placeholder** `GLOSSARY.yml`, tell the
  user, note it on the Linear ticket, and move on. We'll fill it later (for example, when we
  scan their BI tool).

## 3. The first domain

- Explain briefly what a domain is: a business area that groups related entities — e.g.
  sales, marketing, finance, operations.
- Based on the company info you now have, **suggest 2–3 domain options** and let them pick —
  or name their own.
- Create `domains/<name>/` with its `LYNK.md` (what this domain is about).

## 4. The first entities (1–2)

Build one or two entities inside the new domain — follow `references/entity.md`.

Done: the repo has business context, a glossary (or placeholder), one domain, and its first
entities. Suggest validating, then close out the story ticket.
