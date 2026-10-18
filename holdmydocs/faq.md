---
title: FAQ
tags: hmd, getting-started, operations
---

## Before You Start

### Do I need to know Git?

No. Write and save in the browser; HMD records the commits. Start with [[Your First Wiki]].

### Do I need a Git hosting account, AI service or database?

No. The Git repository can stay local and application state is kept in JSON files. Remote hosting, MCP clients and document extraction are optional. [[Install HMD]] starts without them.

### Is HMD a hosted service?

No, it is self-hosted. If someone runs it for your team, you need their wiki address, an account and a namespace you can write in.

### How does search work?

It uses a local index of page titles, bodies and tags, with no external service. Optional document extraction also indexes attachment contents; see [[Attachments]].

### Can anonymous visitors search public pages?

No. Live-wiki search requires login even when pages are public. A static export has its own browser-local search.

### Can I publish documentation without running HMD for readers?

Yes. [[Static Export]] produces a read-only website with navigation and browser-local search. Readers need no account. To update it, export and publish a new snapshot.

## Hosting And Maintenance

### Where is the data stored?

| Directory | Default | Holds |
| --- | --- | --- |
| `HMD_SERVER_REPO_DIR` | `/data/repo` | Pages, attachments, wiki and namespace configuration |
| `HMD_APP_DIR` | `/data/app` | Account state, local configuration, sessions, derived search/model data |

See [[Configuration Reference]] and [[Storage And Recovery]].

### Is the Git remote a backup?

No. It mirrors only pushed commits and not application state. Back up both directories and test recovery; see [[Storage And Recovery]].

### Can I use an SSH remote?

No, remotes are HTTPS-only. Private repositories and authenticated pushes need credentials. See [[Git Sync]].

### Does HMD support real-time collaboration?

No. Each save checks the revision it started from, and a newer revision causes a conflict instead of an overwrite. See [[Pages]].

### What does the health report do?

`/_/health-report` lists missing wiki-link targets, pages with no incoming links and pages unchanged for at least 180 days. `/_/ready` checks deployment readiness. See [[Monitoring And Maintenance]].

### What are the fixed limits?

Ordinary form requests are capped at 2 MiB and namespace exports at 10,000 files. Neither is configurable. See [[Configuration Reference]].

### How do I upgrade?

Stop cleanly, replace the binary or image, then check readiness, login, pages, attachments and sync. See [[Upgrade HMD]].
