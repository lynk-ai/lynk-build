---
name: MCP security — named attacks and their mitigations
description: Tool poisoning, rug pulls, the spec's named attack catalog, and the 2025 CVEs. Read when reviewing a third-party MCP server before installing it, threat-modeling an MCP deployment, building a client that must resist malicious servers, or deciding how much to trust tool descriptions.
labels: [security, tool-poisoning, rug-pull, invariant-labs, confused-deputy, token-passthrough, session-hijacking, ssrf, dns-rebinding, cve, oauth, one-click, threat-model]
---

MCP's threat model has one center of gravity: **the server is not trusted, but the model reads what the server writes.** Every attack below is a variation on that asymmetry, and the mitigations concentrate in the client/host because the architecture gives servers no view into each other or the conversation — isolation is the host's job (see [what-mcp-is](what-mcp-is.md)).

The canonical demonstration is the **Tool Poisoning Attack** — Invariant Labs, April 2025 (invariantlabs.ai disclosure; outlets report the publish day variously between April 1–6, so cite the month only). Hidden instructions embedded in a tool's *description* — visible to the model, invisible in typical UIs — hijack the agent. Their demos included exfiltrating a user's WhatsApp history via a malicious server that "cross-poisons" a *legitimate* WhatsApp MCP server in the same session, and the **rug pull** variant: a server swaps its tool descriptions *after* the user approved them (same disclosure). The spec's counterparts are on the tools page (modelcontextprotocol.io/specification/2025-11-25/server/tools, warning blocks): "clients MUST consider tool annotations to be untrusted unless they come from trusted servers," and clients SHOULD keep human-in-the-loop with the ability to deny invocations. Derived corollary for reviewers: reading a server's *code* isn't enough — read its tool descriptions as prompts, because that's what the model does; and a client that doesn't re-verify descriptions on change is rug-pullable by design.

The spec's Security Best Practices page (modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices — added in 2025-06-18 per that changelog) names and diagrams its own attack catalog; all rows sourced from that page:

| Attack | Mechanism | Spec mitigation |
|---|---|---|
| Confused deputy | MCP proxy with a static third-party client ID + dynamic client registration + consent cookie → attacker skips the consent screen and steals auth codes | Mandatory per-client consent |
| Token passthrough | Server accepts tokens not issued to it — an explicitly forbidden anti-pattern | Don't; validate audience |
| Session hijacking | Guessed/stolen session ID used as identity | Servers MUST NOT use sessions for authentication; bind session IDs to user IDs (`<user_id>:<session_id>`) |
| SSRF via OAuth metadata discovery | Malicious server points the client's metadata fetch at internal targets like 169.254.169.254 | Validate/deny-list discovery targets |
| Local MCP server compromise | Malicious startup command in a one-click install config | Clients MUST show the exact command and get explicit approval |
| OAuth-URL XSS → stdio proxy | XSS in an OAuth URL escalates through a stdio proxy | (named on the page) |

The local-compromise row is the stdout gotcha's security cousin (our call, as framing): the same config file that wires a legitimate server (see [build-a-server](build-a-server.md)) is an arbitrary-command-execution vector when a user pastes a config they didn't read — which is why the mitigation is showing the exact command.

The transport layer carries its own mandate: servers MUST validate the `Origin` header and 403 invalid origins (DNS-rebinding defense, made explicit in 2025-11-25, PR #1439), and local servers SHOULD bind to 127.0.0.1, not 0.0.0.0 (transports page, Security Warning — details in [transports](transports.md)).

None of this is hypothetical — 2025 produced named CVEs in the ecosystem's own tooling (NVD/GHSA entries; attribution below is from the vendors' own disclosures, so treat the who-found-it as vendor-claimed rather than independently verified):

- **CVE-2025-49596** — MCP Inspector <0.14.1 ran with no auth between its web UI and proxy, so a drive-by web page could reach RCE on a developer's machine; CVSS 9.4 (disclosed by Oligo Security, June 2025).
- **CVE-2025-6514** — `mcp-remote` OAuth-endpoint command injection, RCE, CVSS 9.6 (disclosed by JFrog, July 2025).
- **CVE-2025-54136** ("MCPoison", Cursor) — among others the same year (NVD/GHSA).

Derived summary of where that leaves a practitioner: treat every third-party server as untrusted input *and* as code you're executing (both are literally true for stdio servers); treat the developer tooling itself — Inspector, `mcp-remote` — as attack surface and keep it patched; and rely on the client-side controls the spec mandates (consent, command display, origin checks, human-in-the-loop) rather than on server good behavior, which the protocol cannot enforce.
