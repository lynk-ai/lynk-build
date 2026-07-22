---
name: What MCP is — roles, primitives, and the wire protocol
description: The protocol's formal shape — host/client/server roles, the six primitives, JSON-RPC 2.0, and the LSP lineage. Read when you need to know who talks to whom and with what vocabulary before designing, reviewing, or debugging an MCP integration, or when MCP terminology (host vs. client, sampling, elicitation) is ambiguous in a discussion.
labels: [architecture, host, client, server, primitives, resources, prompts, tools, sampling, roots, elicitation, json-rpc, lsp, capability-negotiation]
---

The Model Context Protocol (MCP) is an open protocol for connecting LLM applications to external context and capabilities. Its architecture defines three roles (MCP spec 2025-11-25, main specification page): **Hosts** are the LLM applications that initiate connections; **Clients** are connectors that live *within* the host application, one client per server; **Servers** are the services that provide context and capabilities. Our call: the one-client-per-server detail is the piece most worth internalizing — "client" in MCP is not the end-user application (that is the host) but the per-connection object the host holds. The spec is explicitly modeled on the Language Server Protocol, uses **JSON-RPC 2.0** as its message format, and builds on stateful connections with capability negotiation between the two sides (same source).

The protocol's vocabulary is six primitives, split by which side offers them (MCP spec 2025-11-25, specification overview and lifecycle pages):

| Side | Primitive | What it is |
|---|---|---|
| Server | **Resources** | Context and data for the model or user |
| Server | **Prompts** | Templated messages and workflows for users |
| Server | **Tools** | Functions the model can call |
| Client | **Sampling** | Server-initiated LLM calls — the server asks the *host's* model to generate |
| Client | **Roots** | Server inquiries into the filesystem/URI boundaries it may operate in |
| Client | **Elicitation** | Server-initiated requests for input from the user |

The client-side primitives are what most distinguish MCP from a plain tool-calling API: they let a server call *back* into the host. Alongside the primitives, the spec defines cross-cutting utilities: progress, cancellation, logging, completions, and — added as experimental in the 2025-11-25 revision — tasks (same source; for where tasks went next, see [versions-and-governance](versions-and-governance.md)).

The authoritative definition of all of this is not the prose spec but a TypeScript schema — `schema/2025-11-25/schema.ts` in the modelcontextprotocol/modelcontextprotocol repository — and the spec uses RFC-2119/BCP-14 requirement language (MUST/SHOULD/MAY) throughout (modelcontextprotocol.io/specification/latest, fetched 2026-07-21). When prose and schema seem to disagree, check the schema.

How a connection actually starts, and over which transports it runs, is covered in [lifecycle-and-transports](lifecycle-and-transports.md); why this protocol exists at all is [why-mcp-exists](why-mcp-exists.md).
