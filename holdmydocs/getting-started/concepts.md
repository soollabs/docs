---
title: HMD Concepts
tags: hmd, getting-started
---

You only need a few ideas to find your way around HMD. Start with pages and namespaces; Git and publishing can come later.

## A wiki contains namespaces; namespaces contain pages

A **wiki** is your whole HMD instance. A **namespace** is a top-level area inside it, such as `notes`, `team`, or `handbook`. Each namespace has its own page tree, appearance, and public or private visibility.

A **page** is one Markdown document. Its **slug** is its path inside the wiki:

```text
team/guides/onboarding
│    └─ page path within the namespace
└─ namespace
```

The page lives at `/team/guides/onboarding` in the browser and is stored as `team/guides/onboarding.md` in the content repository. `guides` is an organising folder, not another namespace.

The page's **title** is the name readers see, such as “Onboarding”. Changing the title does not move the page; changing the path does. See [[Pages]].

## Markdown is the content; frontmatter is the metadata

Markdown is plain text with lightweight formatting: `##` starts a section, `-` starts a list item, and `**text**` makes text bold. HMD's editor shows a live preview beside your source.

**Frontmatter** is the small metadata block at the top of a stored Markdown file. It holds values such as the title and tags. The editor's title and tags fields manage those values for you; you do not need to write YAML to create a page. See [[Markdown And The Editor]].

## Links connect your knowledge

A **wiki-link**, such as `[[Onboarding]]`, points to a page by its title. A **backlink** tells you which other pages link to the page you are reading. Together they let you navigate by subject, not just by folder.

Use ordinary Markdown links for external websites. Add **tags** to label related pages across topics. See [[Links And Navigation]].

## Git records your changes

HMD stores content in a local **Git repository**, a directory that also keeps a history of changes. Saving a page creates a **commit**, a recorded revision you can inspect from page history.

A **remote** is an optional second Git repository on a Git host. HMD can push commits to it in the background. You can use HMD without one, and writers do not need to run Git commands to save pages.

A saved page and a successful remote push are different things. A network failure can leave a page safely saved locally but not yet copied to the remote. See [[Git Sync]]. A remote is not a complete backup of your HMD installation; accounts and local settings need a backup too. See [[Storage And Recovery]].

## Reading, writing, and administering are separate permissions

An account can have permission to read pages, write them, or manage settings. Access can also be limited to particular namespaces.

Namespaces are private by default. Making one **public** lets visitors read its ordinary pages and attachments without signing in. Public does not mean editable by everyone. Keep sensitive material in a separate private namespace, and read [[Authentication And Access]] before sharing access.

A **hidden page** is omitted from ordinary navigation and search. Hidden is a filing convention, not a substitute for permissions or a place to store secrets.

## A live wiki and a static site serve different purposes

The running HMD application provides editing, search, accounts, and history. A **static export** is a read-only snapshot of one namespace: HTML pages, styles, scripts, and attachments you can upload to a file host.

Links within that namespace keep working in the export. Its browser-local search covers exported page text; editing and page history need the live application. Changes appear on the static site only after you export and publish again. Its host, not HMD, controls who can read the copy. See [[Static Export]].

## Next steps

- [[Your First Wiki]] — put these concepts into practice.
- [[Namespaces]] — choose how to organise your content.
- [[Running HMD]] — learn what you need to operate an instance.
