---
title: HMD Concepts
tags: hmd, getting-started
---

Start with pages and namespaces; Git and publishing can come later.

## Wikis, namespaces and pages

- **Wiki**: your whole HMD instance.
- **Namespace**: a top-level area such as `notes`, `team` or `handbook`. Each has its own page tree, appearance and public or private visibility.
- **Page**: one Markdown document. Its **slug** is its path inside the wiki.

```text
team/guides/onboarding
│    └─ page path within the namespace
└─ namespace
```

This page is served at `/team/guides/onboarding` and stored as `team/guides/onboarding.md` in the content repository. `guides` is a folder, not another namespace.

The **title** is the name readers see. Changing the title does not move the page; changing the path does. See [[Pages]].

## Markdown and frontmatter

Pages are Markdown. **Frontmatter** is the metadata block at the top of the stored file, holding the title and tags. The editor's title and tags fields manage it, so you never need to write YAML. See [[Markdown And The Editor]].

## Links

- **Wiki-link**: `[[Onboarding]]` points to a page by its title.
- **Backlink**: lists the pages that link to the page you are reading.
- **Tags**: label related pages across topics.
- Use ordinary Markdown links for external sites.

See [[Links And Navigation]].

## Git

HMD stores content in a local **Git repository**. Each save creates a **commit**, which you can inspect from page history. Writers do not run Git commands.

A **remote** is an optional second repository on a Git host, and HMD pushes commits to it in the background. A saved page is not necessarily pushed yet: a network failure leaves it saved locally only. See [[Git Sync]].

For what creates a commit, history and conflicts, see [[Git And History]].

A remote is not a full backup. Accounts and local settings need backing up too. See [[Storage And Recovery]].

## Permissions

Accounts can read pages, write them, or manage settings, and can be limited to particular namespaces.

Namespaces are private by default. A **public** namespace lets visitors read its ordinary pages and attachments without signing in, but not edit them. Keep sensitive material in a private namespace. Read [[Authentication And Access]] before sharing access.

A **hidden page** is left out of navigation and search. It is not access control, so do not store secrets in one.

## Live wiki and static export

The running application provides editing, search, accounts and history. A **static export** is a read-only snapshot of one namespace (HTML, styles, scripts and attachments) that you upload to a file host.

- Links within the namespace keep working.
- Search runs in the browser over exported page text.
- Editing and history need the live application.
- Changes appear only after you export and publish again.
- The file host controls who can read it.

See [[Static Export]].

## Next steps

- [[Your First Wiki]]: put these concepts into practice.
- [[Namespaces]]: choose how to organise your content.
- [[Running HMD]]: what you need to operate an instance.
