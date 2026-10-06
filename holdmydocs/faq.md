---
title: FAQ
tags: hmd, operations
---

Answers to common questions before you start using or hosting HMD.

## Do I need to know Git to use HMD?

No. Write and save in the browser; HMD records the commits for you. Git knowledge helps if you want to manage the repository outside HMD or resolve divergent remote histories. Start with [[Your First Wiki]].

## Do I need a Git hosting account or an AI service?

No. HMD can keep its Git repository entirely local. A remote Git host, MCP clients, and document extraction are optional integrations, not requirements for a working wiki. [[Install HMD]] starts without them.

## Is HMD a hosted service?

HMD is self-hosted: you run the application on hardware or infrastructure you control. If someone runs it for your team, you only need their wiki address and an account. The host is responsible for updates, backups, and access controls.

## Can I publish documentation without running HMD for readers?

Yes. [[Static Export]] produces a read-only website with page navigation and browser-local page search. Readers need no HMD account. Publishing an update means exporting and uploading a new snapshot.

## Where is HMD data stored?

Two directories, both configurable at first start:

- `HMD_REPO_DIR` (default `/data/repo`) — the Git repository holding pages, attachments, and wiki and namespace configuration.
- `HMD_APP_DIR` (default `/data/app`) — accounts (`users.json`), local configuration (`config.yaml`), active sessions, the search index, and the downloaded embedding model.

See [[Configuration Reference]] and [[Storage And Recovery]].

## Is the Git remote a backup?

No. The remote mirrors commits that HMD has already pushed, and a failed push leaves local commits un-pushed. Nothing replicates `app` (accounts, configuration, secrets). Back up both directories yourself and test the restore: [[Storage And Recovery]].

## Can I use an SSH remote?

No. Remotes are HTTPS-only and authenticate with a user name and personal access token. SSH remotes are not supported. See [[Git Sync]].

## Does HMD support real-time collaboration?

No. HMD uses optimistic locking: each save checks the page hash it was based on, and a page changed on disk since then shows the conflict screen instead of overwriting it. See [[Pages]].

## How does search work?

Search uses HMD's built-in full-text index of page titles, bodies, and tags. It is local and needs no external service. With document extraction enabled (opt-in Tika), attachment contents are indexed too. See [[Configuration Reference]].

## What does the health report do?

`/_/health-report` lists wiki-linked but missing pages, orphaned pages with no incoming links, and pages unchanged for at least 180 days. It is a hygiene report for editors, not a liveness check — use `/_/ready` for that. See [[Monitoring And Maintenance]].

## Can anonymous users search public pages?

On the live wiki, search requires login even when the pages are public. A static export has its own browser-local search of the exported pages; it does not call the live wiki's `/_/search` route.

## What are the fixed limits?

Several limits are intentionally not configurable, from the 2 MiB ordinary form request to the 10,000-file namespace export ceiling. The full table is in [[Configuration Reference]].

## Can I export a namespace?

Yes. Export a namespace from its settings page to generate a static version of its documentation that needs no running HMD to serve. See [[Static Export]].

## Do I need a database?

No. HMD's state is a Git repository plus JSON files under `HMD_APP_DIR`. There is no separate database to install, back up, or tune.

## How do I upgrade?

Stop cleanly, replace the binary or image while stopped, and run the readiness, login, page, attachment, and sync checks afterwards. See [[Upgrade HMD]].
