---
title: Attachments
tags: hmd, writing
---

Upload files and images to a page.

## Upload a file

1. Open the page in the editor.
2. Click **attach** in the toolbar and choose a file, or paste or drag an image into the editor. Pasting and dragging are image-only. The button offers images and common office documents, but the server accepts any file.
3. The link is inserted at the cursor: `![file](url)` for an image, `[file](url)` for anything else.

   ![An uploaded walking-route image linked in the editor](/_/attachments/holdmydocs/writing/attachments/upload.png)

4. Save the page. Uploading does not save it.

## Where attachments live

A page slug is its address without a leading slash or `.md`, such as `notes/inbox`; see [[HMD Concepts]].

- Stored at `<namespace>/.attachments/<page>/<file>` in the content repository and served at `/_/attachments/<page-slug>/<file>`.
- Each upload is a commit, so attachments share the page's Git history.
- Filenames are sanitised: the base name is kept, the name part is slugified and the extension is lower-cased. There is no extension allowlist.
- The default maximum upload size is 10 MiB. An administrator can change it.
- Renaming a page does not move its attachments. They keep the slug they were uploaded under.

## Move old attachments

Earlier versions kept attachments in a top-level `attachments/` folder. HMD still serves them and shows administrators a banner until they are moved.

1. Update every HMD instance that uses the repository. Older versions only look in the old folder.
2. Open **Settings → Wiki**. It lists each namespace that still has files there, with a count.
3. Click **Move attachments**. This moves them into their namespaces in one commit. URLs do not change.

Files of a deleted namespace cannot be moved. Delete them from the same list. They stay in Git history.

## Inline rendering

Only PNG, JPEG, GIF and WebP render inline. Every other type is sent as a download with a `nosniff` header, so uploaded HTML or SVG never executes in the wiki.

## Search and extraction

- Plain UTF-8 `.txt` and `.md` uploads always get cached text extraction (a sidecar file), so MCP and attachment search can read them.
- For PDF, Word, spreadsheets and similar, set `document_search.tika_url` to a private Apache Tika endpoint on the Document search settings page, or override it with `HMD_DOCUMENT_SEARCH_TIKA_URL`, then restart. HMD then indexes their text for keyword and semantic search.
- Without Tika, those files are stored but not indexed.

## Access control

Attachments follow their page's namespace access policy. Public namespaces are readable anonymously. Private ones require authentication, and an anonymous visitor gets the same result as for a missing attachment.

## Next steps

[[Pages]], [[Markdown And The Editor]], [[MCP Integration]].
