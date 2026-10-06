---
title: Your First Wiki
tags: hmd, getting-started, tutorial
---

Create a small project wiki with two linked pages, then use page history to check an edit. By the end, you'll know the everyday HMD workflow: write, save, link, and find your work again.

You need a running HMD instance and an account that can write pages. If you are hosting it yourself, complete [[Install HMD]] and [[First-Run Setup]] first. If someone else runs it, ask them for the wiki address, an account, and a namespace you can write in.

The examples use a namespace named `notes`. Substitute your namespace if it has a different name. You do not need a Git remote or an AI assistant for this guide.

This is what the editor looks like. Your page's title and content will differ:

![Split-pane editor in a fictional homelab wiki](/_/attachments/holdmydocs/writing/pages/editor.png)

## 1. Create a project page

1. Open your namespace and click **New** in the top bar.
2. Set the **path** to `notes/weekend-project`. The path is the page's address; do not add `.md` in this field.
3. Set the **title** to `Weekend Project` and **tags** to `project`.
4. Paste this into the left editor pane:

   ```markdown
   # Weekend Project

   Build a small website for our walking group.

   ## Plan

   - [ ] Choose a name
   - [ ] Add the next walk
   - [ ] Share the website with the group

   ## Notes

   Keep the first version simple: a welcome page and a list of walks.
   ```

5. Check the preview, then click **Save**, or press **Ctrl+S** (**Cmd+S** on macOS).

You now have a page at `/notes/weekend-project`. It appears in the namespace's page tree. HMD has saved a Markdown file and recorded the creation in Git; you do not need to run Git commands yourself.

## 2. Add a second page

Click **New** again. Use the path `notes/launch-checklist`, the title `Launch Checklist`, and the tag `project`. Paste and save:

```markdown
# Launch Checklist

Before sharing the website:

- [ ] Check the date and meeting point
- [ ] Test the website on a phone
- [ ] Ask someone else to read the welcome page

Part of [[Weekend Project]].
```

On the saved page, **Weekend Project** is a link. Click it to return to your first page. The double brackets make a **wiki-link**: HMD finds the page by its title, rather than requiring you to type its URL.

## 3. Link the pages in both directions

On **Weekend Project**, click **Edit**. Add this below the notes:

```markdown
Ready to share? Work through [[Launch Checklist]].
```

Save, then follow the new link. You can now move between the overview and the checklist without going back to the page tree.

Use the exact page title inside the brackets. A link to a page that does not exist yet appears as a missing link in the live wiki; see [[Links And Navigation]].

## 4. Make an edit and find it in history

1. Edit **Launch Checklist** and change one `[ ]` to `[x]`.
2. Save. The rendered page now shows that task as complete.
3. Open **history** on the page.
4. Open the earlier revision with **view** to see the unchecked task.
5. Choose **View current version** to return to the latest page.

Every save creates a revision. If you need to undo an edit, **revert** restores an older version as another new revision; it does not erase the history. See [[Pages]] for the full editing and recovery guide.

## 5. Find your work again

Use the search icon in the top bar to search for `walking group`. Search reads page text as well as titles, so you do not need to remember the exact name. You can also use the page tree to browse both pages.

This search belongs to your running HMD instance. The static documentation site you are reading is a separate, read-only export.

## What you've learned

- A **page** has a path, a display title, and Markdown content.
- A **namespace** groups pages; `notes` is the namespace in both example paths.
- A **wiki-link** connects pages by title.
- **Save** records the page and its history in Git.

You can keep these pages as a starting point, or replace the example content with your own project. Neither page is public unless the namespace is public.

## Next steps

- [[HMD Concepts]] — understand pages, namespaces, Git, and publishing.
- [[Markdown And The Editor]] — add formatting, tables, and diagrams.
- [[Attachments]] — add screenshots and supporting files.
- [[Static Export]] — publish a read-only copy when your documentation is ready.
