---
title: Namespaces
tags: hmd, writing
---

A namespace is a separate area of the wiki, such as `notes`, `team` or `handbook`. Each has its own pages, navigation, look and visibility. Use one per project or audience.

The namespace is the first part of a page's address. In `team/guides/onboarding`, `team` is the namespace and `guides` is a folder inside it. Namespaces do not nest.

## Create a namespace

1. Open **Settings → Namespaces** and click **New namespace**.
2. Enter a short name without spaces or slashes, such as `team`.
3. Save. The namespace is private until you make it public.

## Change a namespace

Open **Settings → Namespaces** and click **Edit** next to it.

| Section | What you can change |
| --- | --- |
| General | Description, homepage (**index page**), page order in the sidebar and quick-create template |
| Published | Whether anyone can read it without signing in, how it looks to them and its link preview image |
| Static site | Settings for exporting it as a website, see [[Static Export]] |
| Widgets | What appears in the sidebar, see [[Namespace Configuration Reference]] |

**Reset namespace settings** puts these back to the defaults and keeps every page.

## Public or private

Visibility covers the whole namespace, never single pages. A public namespace lets anyone read every page and attachment in it without signing in. Keep anything internal in a separate private namespace.

## Link previews

When someone shares a page from a public namespace or a static export, chat apps and social networks show a preview card. HMD fills it in from the page:

- The description is the page's first paragraph, shortened to about 155 characters. A page without text uses the namespace description.
- The image is the first PNG or JPEG attached to the page. Pages without one use the namespace's **link preview image**, chosen under **Published** from the namespace's attachments.

Keep preview images under 300 KB, or WhatsApp leaves them out. Public pages only get preview cards when the server has a `server.base_url`.

## Quick-create pages

Give a namespace a quick-create template and `ctrl-j` (`cmd-j` on macOS) opens a new page from it, named automatically. This suits a daily log or meeting notes. Set it under **General**; the template is a hidden page you write once. [[Namespace Configuration Reference]] has the naming patterns.

## Delete a namespace

**Delete namespace** removes the namespace and every page and file in it. It asks you to confirm first. Deleted pages stay in Git history, but no longer appear in the wiki.

## Next steps

[[Pages]], [[Static Export]], [[Settings And Administration]].
