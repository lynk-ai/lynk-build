---
name: What MCP is — architecture and design principles
description: The host/client/server architecture, the 1:1 session rule, the JSON-RPC base, and the six primitives. Read when you need the mental model before touching any MCP code, or when confused about which component (host, client, server) owns a responsibility.
labels: [architecture, host, client, server, json-rpc, sessions, design-principles, primitives, isolation]
---

The Model Context Protocol (MCP) is an open protocol for connecting AI applications to external tools and data. Its architecture, per the spec's architecture page (modelcontextprotocol.io/specification/2025-11-25/architecture), has three roles: a **host** (the AI application — a chat app, an IDE, an agent runtime), which spawns one or more **clients**, each of which holds a session to exactly one **server** (the integration exposing tools or data). The client-to-server relationship is a strict **1:1 session** — a host that talks to five servers runs five clients. All messages are JSON-RPC 2.0 (same source).

The part of this worth internalizing — because it explains many otherwise-odd protocol decisions — is the spec's stated design principles (architecture page, Design Principles section, quoted): "servers should be extremely easy to build" and "servers should not be able to read the whole conversation, nor 'see into' other servers." Conversation history stays with the host; a server sees only what the host's client explicitly sends it. Derived consequence: isolation between servers is a *host* responsibility, not something servers can enforce for themselves — which is why cross-server attacks are a real category (see [security](security.md)).

The protocol's surface is six primitives, split by which side offers them. Three are server-side — **tools**, **resources**, **prompts** — and three are client-side — **sampling**, **roots**, **elicitation**. The full treatment, including who controls each, is in [server-primitives](server-primitives.md); how a session starts and negotiates which primitives are actually available is in [protocol-lifecycle-and-versioning](protocol-lifecycle-and-versioning.md); how the bytes move is in [transports](transports.md).

One naming trap worth flagging (derived from the architecture above): "client" in MCP means the protocol-side connector inside the host application, not the end user's app as a whole. Docs and error messages use it in that narrow sense, so "the client MUST echo the session header" is an obligation on your host framework's MCP connector, not on your end users.
