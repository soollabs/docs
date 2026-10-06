---
title: Limitations
tags: hmd, reference
---

- HMD does not provide real-time collaborative editing, live cursors, or shared buffers. Concurrent saves use optimistic locking instead.
- Git remotes use HTTPS authentication; SSH remotes are unsupported.
- Namespaces are top-level only. Deeper folders organise pages but have no namespace semantics.
- MCP can upload attachments and read cached extracted text, but cannot browse attachment directories or access hidden pages or `.wiki.yaml`.
- Attachment search requires an operator-supplied Apache Tika Server and only covers formats it can extract.
- Static exports provide browser-local page search, not the live instance's search filters or attachment-content search. Editing, accounts, and history are not included.
- Bidirectional sync only fast-forwards. Resolve divergent Git histories outside HMD before resuming writes.
