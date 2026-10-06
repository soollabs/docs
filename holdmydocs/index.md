---
title: Hold My Docs
tags: hmd, documentation
---

**A wiki you host. Markdown you own. History you can trust.**

![A fictional HMD wiki on a desktop and phone](/_/attachments/holdmydocs/index/hero.png)

Hold My Docs (HMD) is a place to write, find, and share documentation in your browser. Use it for a personal knowledge base, a team's internal guides, or a public documentation site like this one.

HMD stores your pages as Markdown files in a Git repository. You get a web editor, search, and page history without giving up ordinary files you can back up, edit with other tools, or take elsewhere. You do not need to know Git to write in HMD.

**New here?** If someone already runs HMD for you, start with [[Your First Wiki]]. If you're setting it up yourself, follow [[Install HMD]] and [[First-Run Setup]] first. You'll create two linked pages, make an edit, and find it in history.

## Why HMD?

### Write in the browser, keep your files

Write Markdown with a live preview. Add images, files, tables, and diagrams. Every save records a Git commit, so you can see what changed and restore an earlier version without losing the intervening history.

### Turn separate notes into useful documentation

Link pages by title with wiki-links, follow backlinks to related material, and search titles, text, and tags. Group projects into **namespaces**: separate areas of the wiki with their own navigation, appearance, and visibility.

### Choose who can read—and where you publish

Keep a namespace private, let visitors read it without signing in, or export it as a static website. Static exports need only a file host, not a running HMD server. This documentation site is one of those exports.

### Give assistants a shared source of knowledge

Connect an AI assistant through **MCP**, a protocol that lets assistants use external tools. Give it permission to read selected namespaces or help maintain pages. You control its access; changes remain in the same Git history as human edits. See [[MCP Integration]].

## Start with what you want to do

- **Build a personal wiki.** Follow [[Your First Wiki]], then learn [[Links And Navigation]] to connect your notes.
- **Document a project or team.** Start with [[Namespaces]], then configure [[Authentication And Access]] before inviting readers and writers.
- **Publish product documentation.** Organise your page tree and homepage, then follow [[Static Export]] to publish a read-only site.
- **Keep knowledge for an AI assistant.** Start with [[MCP Integration]] and the [[LLM Wiki]] example.

## Explore the documentation

- [[Getting Started]] — installation, a hands-on tutorial, and the core concepts.
- [[Writing And Organising]] — pages, Markdown, links, images, and namespaces.
- [[Running HMD]] — configuration, accounts, Git sync, backups, and upgrades.
- [[Integrations]] — reverse proxies, AI assistants, and static publishing.
- [[Reference]] — exact configuration keys, API endpoints, and MCP tools.

## Is HMD right for you?

HMD runs as a single Go application. You can start with local storage and add a Git remote later; no separate database service is required. Self-hosting means you are responsible for updates, access controls, and backups.

HMD is not a real-time collaborative editor: two people can edit, but conflicting saves need to be resolved. Git remotes use HTTPS, not SSH. Check [[Limitations]] and [[FAQ]] before planning your deployment.

**Ready to try it? [[Install HMD]], then create [[Your First Wiki]].**
