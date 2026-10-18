---
title: Limitations
tags: hmd, reference
---

- No real-time collaborative editing, live cursors or shared buffers. Concurrent saves use optimistic locking.
- Git remotes need HTTPS authentication. SSH remotes are unsupported.
- Namespaces are top-level only. Deeper folders organise pages but are not namespaces.
- MCP can upload attachments and read cached extracted text. It cannot browse attachment directories or access hidden pages or `.wiki.yaml`.
- Attachment search needs an operator-supplied Apache Tika Server and only covers formats Tika can extract.
- Static exports have browser-local page search only: no search filters or attachment-content search. They exclude editing, accounts and history.
- Bidirectional sync only fast-forwards. Resolve divergent Git histories outside HMD before resuming writes.
