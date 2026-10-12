---
title: FAQ
tags: hmd, getting-started, operations
---

## Before You Start

### Do I need to know Git?

No. Write and save in the browser; HMD records commits for you. Start with [[Your First Wiki]]. Git knowledge helps when managing the repository outside HMD or resolving divergent remote histories.

### Do I need a Git hosting account, AI service or database?

No. HMD can keep its Git repository entirely local, with application state in JSON files. Remote hosting, MCP clients and document extraction are optional. [[Install HMD]] starts without them.

### Is HMD a hosted service?

HMD is self-hosted: you run it on hardware or infrastructure you control. If someone runs it for your team, you need only their wiki address, an account and a namespace you can write in. The host handles updates, backups and access controls.

### How does search work?

Search uses a local index of page titles, bodies and tags. It needs no external service. Optional document extraction also indexes attachment contents; see [[Attachments]].

### Can anonymous visitors search public pages?

Live-wiki search requires login even when pages are public. A static export has its own browser-local search and does not call the live wiki.

### Can I publish documentation without running HMD for readers?

Yes. [[Static Export]] produces a read-only website with navigation and browser-local search. Readers need no account. Updates require exporting and publishing a new snapshot.

## Hosting And Maintenance

### Where is the data stored?

Two directories: `HMD_SERVER_REPO_DIR` (default `/data/repo`) holds pages, attachments and wiki/namespace configuration; `HMD_APP_DIR` (default `/data/app`) holds account state, local configuration, sessions and derived search/model data. See [[Configuration Reference]] and [[Storage And Recovery]].

### Is the Git remote a backup?

No. It mirrors only commits already pushed. Failed pushes leave local commits unmirrored, and Git does not replicate application state. Back up both directories and test recovery; see [[Storage And Recovery]].

### Can I use an SSH remote?

No. Remotes are HTTPS-only. Public clones need no token; private repositories and authenticated pushes need suitable credentials. See [[Git Sync]].

### Does HMD support real-time collaboration?

No. Each save checks the revision it started from; a newer revision causes a conflict instead of being silently overwritten. This is **optimistic locking**. See [[Pages]].

### What does the health report do?

`/_/health-report` lists missing wiki-link targets, pages with no incoming links and pages unchanged for at least 180 days. Use `/_/ready` to check deployment readiness. See [[Monitoring And Maintenance]].

### What are the fixed limits?

Some limits are intentionally not configurable, including the 2 MiB ordinary form request and 10,000-file namespace export ceiling. See [[Configuration Reference]].

### How do I upgrade?

Stop cleanly, replace the binary or image and check readiness, login, pages, attachments and sync afterwards. See [[Upgrade HMD]].
