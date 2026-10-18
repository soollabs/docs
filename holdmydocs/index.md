---
title: Hold My Docs
tags: hmd, documentation
---

**A wiki you host. Markdown you own. History you can trust.**

![A fictional HMD wiki on a desktop and phone](/_/attachments/holdmydocs/index/hero.png)

Hold My Docs (HMD) is a browser-based place to write, find and share documentation: a personal knowledge base, a team's internal guides or a public docs site like this one. Pages are Markdown files in a Git repository, so you can back them up or edit them with other tools. You do not need to know Git.

**New here?** If someone runs HMD for you, start with [[Your First Wiki]]. To set it up yourself, follow [[Install HMD]] and [[First-Run Setup]] first.

## What you get

- **Web editor.** Markdown with a preview, images, files, tables and diagrams. Every save is a Git commit, so you can see changes and restore earlier versions.
- **Linked pages.** Wiki-links, backlinks, and search across titles, text and tags.
- **Namespaces.** Separate areas of the wiki with their own navigation, appearance and visibility.
- **Access control.** Keep a namespace private, let visitors read it without signing in, or export it as a static website that needs only a file host. This site is one of those exports.
- **AI assistants.** Connect an assistant through MCP with read or maintain permissions on selected namespaces. Its changes go into the same Git history. See [[MCP Integration]].

## Start with what you want to do

- **Personal wiki.** Follow [[Your First Wiki]], then [[Links And Navigation]].
- **Project or team docs.** Start with [[Namespaces]], then configure [[Authentication And Access]] before inviting people.
- **Public product docs.** Follow [[Static Export]] to publish a read-only site.
- **Knowledge for an AI assistant.** Start with [[MCP Integration]] and the [[LLM Wiki]] example.

## Explore the documentation

- [[Getting Started]]: installation, a tutorial and core concepts.
- [[Writing And Organising]]: pages, Markdown, links, images and namespaces.
- [[Running HMD]]: configuration, accounts, Git sync, backups and upgrades.
- [[Integrations]]: reverse proxies, AI assistants and static publishing.
- [[Reference]]: configuration keys, API endpoints and MCP tools.

## Is HMD right for you?

- HMD is a single Go application. Start with local storage and add a Git remote later; no separate database is needed.
- You are responsible for updates, access controls and backups.
- It is not a real-time collaborative editor: conflicting saves must be resolved.
- Git remotes use HTTPS, not SSH.

See [[Limitations]] and [[FAQ]] before planning a deployment.

Next: [[Install HMD]], then [[Your First Wiki]].
