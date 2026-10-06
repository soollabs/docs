---
title: First-Run Setup
tags: hmd, getting-started
---

Give your wiki a name and create a place for its pages. This is a one-time administrator task after [[Install HMD]]; people joining an existing wiki can start with [[Your First Wiki]] instead.

A **namespace** is a top-level area of your wiki, such as `notes` or `team`. Start with one. You can add more later to separate projects or audiences.

## 1. Sign in

Open your HMD address and sign in with the administrator credentials you supplied during installation. On a fresh instance, HMD opens the setup screen.


Nothing is written until you click **Add selected**.

## 2. Name the wiki and its first namespace

For a simple personal wiki, use:

| Field | Example | What it controls |
| --- | --- | --- |
| site name | `My Wiki` | The name shown in the top bar |
| default namespace | *create a new namespace* | Where the wiki opens after sign-in |
| new namespace | `notes` | The first segment of your page addresses |

Use a short namespace name without spaces or slashes. `notes`, `team`, and `homelab` work; `my notes` and `notes/inbox` do not.

Leave **Help guide** selected on a fresh installation. It adds an in-app guide to the editor and Markdown conventions. If a guide already exists, selecting this option replaces it; leave it unchecked to keep your existing guide.

## 3. Create the wiki

Click **Add selected**. HMD creates the selected items and opens the namespace's welcome page. You should see your site name in the top bar and the welcome page in the page tree.


The new namespace is private by default. Creating it does not publish your content to the internet.

Sign out and sign in again to confirm that the wiki opens in the right place. You are now ready to write: continue with [[Your First Wiki]].

## If you already have content

The setup screen adapts to what is missing. You may see an existing namespace selector, a **First namespace** option, or only the option to add a help guide. Selecting an existing namespace as the default does not replace its pages.

An administrator can reopen setup from **Settings** at `/_/settings`. You can also skip setup and return later; skipping does not create any of the missing items.

## Where these settings are stored

You do not need to edit files to complete setup. For administrators managing the content repository directly, the selected options can create:

- `.wiki.yaml` — site name and default landing destination.
- `notes/.namespace.yaml` — namespace settings, including its welcome page index.
- `notes/readme.md` — the welcome page in the example namespace.
- `readme.md` — an introduction for the Git repository's front page, not a wiki page.
- `.help.md` — the hidden in-app help guide, if selected.

The actual namespace path uses the name you chose. Wiki and namespace settings travel with the content repository. Application settings and accounts stay in the separate application-state directory. See [[Configuration]] when you need to change those settings.

## Next steps

**Create [[Your First Wiki]]** to practise writing, linking, and using history. For a plain-language explanation of the terms, read [[HMD Concepts]].
