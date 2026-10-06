---
title: Pages
tags: hmd, writing
---

Create, edit and version pages in the split-pane editor, and recover older versions from history.

## Create and edit a page

You need a signed-in account with write access to the namespace. For a worked example with content to copy, follow [[Your First Wiki]].

1. Click **New** in the top bar.

   The editor opens for a new page in the current namespace. The path field is pre-filled with a slug such as `homelab/new`; change it to the page slug you want. With a namespace that declares a quick-create template, `ctrl-j` (`cmd-j` on macOS) and the command palette's `>new` verb open the editor pre-filled from that template instead.

2. Set the **path**, **title** and **tags** in the editor's top row.

   The path is the page slug, for example `homelab/servers`. The title is the display name; tags are comma-separated. The **hidden** checkbox files the page as a hidden page, excluded from the page list, search, tags and backlinks.

3. Write the page in the left pane. The right pane renders a live preview as you type.

   ![Split-pane editor in a fictional homelab wiki](/_/attachments/holdmydocs/writing/pages/editor.png)

4. Save with **Save** in the top bar or `ctrl-s` (`cmd-s` on macOS).

   You should now see the rendered page. HMD stored one Markdown file per page and committed the save: new pages produce `Create` commits, edits produce `Update` commits, and changing the path during the same edit records a `Move`.

## What HMD wrote

Each page is one Markdown file, `<slug>.md`, with the title and tags in frontmatter:

```markdown
---
title: Servers
tags: homelab, hardware
---

# Servers

...
```

The title and tags fields in the editor write this frontmatter for you. A `pin: true` frontmatter line is also honoured by the pinned widget. Every save is a Git commit, so the repository history is the page history.

## Read pages in order

Use **Previous** and **Next** at the bottom of a page to move through its namespace in page-tree order. These links work for signed-in readers, public readers, and static exports. They stay within the current namespace and only include pages you can access.

## History and revert

1. Open a page and choose **history**, or visit `/<slug>?do=history`.

2. Review the revisions: short hash, commit message, author and date. The current revision is marked.

3. Select a revision and choose **revert**, or use the **view** link to read an old version first.

Revert writes the old content as a new commit (`Revert <slug> to <short hash>`). It never rewrites or deletes earlier commits, so anything in history stays recoverable.

## When two people edit the same page

If someone else saves the page after you open it, HMD asks you to resolve the conflict rather than silently overwriting their work. This is called **optimistic locking**: your editor remembers which revision you started from.


The screen shows the other writer's revision (**theirs**) and your unsaved draft (**yours**). Open **view newer version** to compare, or **overwrite with mine** to replace the newer content with your draft. Every save is a commit, so either choice is recoverable from history.

## Common pitfalls

- Opening the editor does not create a page. A page exists only after a save.
- `ctrl-j` needs a quick-create template: the namespace must declare a `new:` block in `.namespace.yaml`. Without one, use **New** in the top bar.
- The path field, not the title, decides the slug. Two pages can share a display title, but each slug is unique.

## Next steps

[[Markdown And The Editor]], [[Links And Navigation]], [[Attachments]].
