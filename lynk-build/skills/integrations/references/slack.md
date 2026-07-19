# Slack — usage

Slack is the team chat connection — use it to find context in conversations and to post
messages.

**Use the project's dedicated channel only** — the channel chosen during setup (see
`slack-setup.md`). That's where users report issues and where status updates belong. Do not
search, read, or post in other channels unless the user explicitly asks.

If Slack isn't connected, see `slack-setup.md`.

## What you can do

Once the Slack MCP server is connected, its actions are available as tools. The common ones:

- **Read & search:** read the channel's recent messages or a specific thread; search within
  it for past reports on the same topic (past threads are reference material, like past
  Linear tickets).
- **Post:** reply in the reporter's thread in the channel (and schedule/draft messages).
  Prefer thread replies over new channel messages — keep each issue's conversation in one
  thread.

## How it relates to Linear

Linear is the system of record (see the operating contract → "Task tracking"); Slack is the
human surface. A report in the channel becomes a Linear ticket; status is read from Linear + the
PR, never from Slack. Reactions are decoration — never treat them as status or approval.

## Important: posting is public

Sending a Slack message is **visible to other people and hard to take back**. Treat it like any
externally-visible action:

- **Confirm before sending** — show the user the exact text and the target thread, and get a
  clear go-ahead. Don't post unprompted.
- Prefer drafting first when there's any doubt.
- Reading and searching are safe and don't need confirmation.
