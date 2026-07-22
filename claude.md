# lynk-build — project guidance

## Library search → write offer (user decides; never automatic)

When a library research request runs through `lynk-build:lynk-research`, and the result is thin, do **not** silently
stop and do **not** auto-write. Surface the concrete result first, then let the
user decide what to do about the gap:

- **No relevant books** (`lynk-research` returned nothing / "your library
  doesn't cover this") → tell the user there's no coverage, then **offer** to
  write a new book on the topic.
- **Partial coverage** (some chapters matched but they don't fully answer the
  question) → give the cited partial answer, then **offer** to edit an existing
  chapter or add a new one to the book that already owns the area.
- **Fully answered** → just answer with citations. No offer.

Only if the user accepts, invoke the **`book-writer`** skill. Hand it a brief:

- the user's ask, verbatim
- what `lynk-research` searched and what it actually returned — the concrete
  result (empty, or the partial hits with their `book · chapter` citations)
- the specific gap to fill
- the target book/chapter, if the partial result already points at one

The decision is the user's, made *after* seeing concrete search results — the
write is never triggered automatically off a search miss. The writer promotes
approved content into `lynk-build/library/`, the same store `lynk-research`
reads, so anything written becomes immediately findable by the reader.
