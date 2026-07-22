---
name: Security pitfalls — the spec's named attack classes and tool poisoning
description: The normative attack catalog from the spec's Security Best Practices document, plus the demonstrated tool-poisoning attack. Read when reviewing an MCP integration for security, deciding whether to trust a third-party server, building an MCP proxy or gateway, or handling OAuth/sessions in a server.
labels: [security, attacks, confused-deputy, token-passthrough, ssrf, session-hijacking, tool-poisoning, prompt-injection, oauth, consent, invariant-labs, whatsapp, mcptox, owasp]
---

MCP's spec does something unusual: it ships a normative **Security Best Practices** document with named attack classes (modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices — source for the entire table below). If you build or review MCP infrastructure, this catalog is the checklist:

| Attack class | Mechanism and required defense |
|---|---|
| **Confused Deputy** | MCP proxy servers with static third-party client IDs + consent cookies let attackers mint tokens without consent; per-client consent is a MUST |
| **Token Passthrough** | Explicitly forbidden anti-pattern: accepting tokens not issued to the MCP server |
| **SSRF** | Via OAuth metadata discovery URLs — cloud metadata endpoints, DNS rebinding |
| **Session Hijacking** | Servers MUST NOT use sessions for authentication; session IDs must be non-deterministic and SHOULD be bound as `<user_id>:<session_id>` |
| **Local MCP Server Compromise** | Malicious startup commands in one-click config; the exact command must be shown untruncated for consent |
| **OAuth Authorization URL Validation** | Reject `javascript:`/`data:`/`file:` schemes; never shell out to open URLs |
| **stdio Transport in Proxy Scenarios** | XSS → proxy token theft → RCE escalation chain |
| **Scope Minimization** | Request the narrowest scopes that work |

Above the catalog, the main spec makes two trust rulings of its own (MCP spec 2025-11-25, Security and Trust & Safety section): tool descriptions and annotations "should be considered untrusted, unless obtained from a trusted server," and explicit user consent is required before any tool invocation or sampling. That first ruling is the protocol-level acknowledgment of prompt-injection risk — and it is not theoretical.

**Tool poisoning, demonstrated.** In April 2025, Invariant Labs showed a malicious MCP server whose *tool description* carried hidden instructions that made an agent exfiltrate a user's entire WhatsApp history — through a *legitimate* whatsapp-mcp server the user had also installed — padding the output with whitespace to hide the exfiltration in the UI (Invariant Labs, via Docker's "MCP Horror Stories" writeup; reproduction code public at github.com/invariantlabs-ai/mcp-injection-experiments; the original Invariant blog-post URL was not fetched directly, so cite the repo for the mechanism). The attack's key property (derived from the mechanism above): the poisoned server never touches your data — it only speaks; the damage is done by the agent wielding your other, legitimate tools. Auditing what a server's tools *do* is therefore insufficient; what their descriptions *say* is attack surface.

The attack class has since been institutionalized: it spawned an academic benchmark (MCPTox, arXiv:2508.14925); OWASP cites it in the December 2025 Agentic Top 10 (per the same secondary coverage — not verified against the OWASP document itself); and Microsoft issued its own warning about poisoned MCP tool descriptions in June 2026 (The Hacker News, June 2026).

Practical consequences for the earlier chapters (derived from the catalog + tool poisoning): treat installing a third-party server like installing a shell extension, not like adding an API key — the config formats in [test-and-connect](test-and-connect.md) execute arbitrary local commands, which is exactly the Local MCP Server Compromise vector; and if you publish a server ([build-a-server](build-a-server.md)), your tool descriptions are part of your security posture, because every host will feed them to a model.
