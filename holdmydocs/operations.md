---
title: Running HMD
tags: hmd, operations
---

Hosting HMD means looking after two things: the Git-backed content repository and the local application state. Start with a private local instance, then add network access and integrations deliberately.

## Prepare a deployment

1. [[Install HMD]] — create the application and its persistent storage.
2. [[Configuration]] — choose where settings live and how to apply them.
3. [[Authentication And Access]] — set up accounts and choose permissions.
4. [[Reverse Proxies]] — serve HTTPS and configure trusted proxy headers.
5. [[Storage And Recovery]] — back up both data directories and test a restore.

## Operate it day to day

- [[Git Sync]] — connect an HTTPS remote and understand local saves, background pushes, and optional bidirectional sync.
- [[Monitoring And Maintenance]] — check readiness, sync status, and broken links.
- [[Troubleshooting]] — diagnose startup, sign-in, save, and sync failures.
- [[Upgrade HMD]] — replace the application safely and verify the result.

## Manage people and integrations

- [[Settings And Administration]] — personal settings versus administrator controls.
- [[Personal Access Tokens]] — create scoped credentials for API and MCP clients.
- [[Security Architecture]] — understand trust boundaries and deployment protections.

For exact keys, defaults, and environment variables, use [[Configuration Reference]].
