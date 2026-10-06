---
title: Attachments
tags: hmd, writing
---

Upload files and images to a page, and control how they are stored, served and searched.

## Upload a file

1. Open the page in the editor.

2. Click **attach** in the toolbar and choose a file, or paste or drag an image straight into the editor.

   Pasting and dragging are image-only. The attachment button accepts images and common office documents, and the server accepts any file.

3. The upload inserts the link at the cursor: `![file](url)` for an image, `[file](url)` for anything else.

   You should now see the markdown link in the editor and, for an image, the rendered image in the preview:


4. Save the page.

## Where attachments live

HMD stores the file at `attachments/<page-slug>/<file>` in the content repository and serves it at `/_/attachments/<page-slug>/<file>`. Uploading is itself a commit, so attachments share the page's Git history.

Filenames are sanitised on upload: the base name is kept, the name part is slugified and the extension is lower-cased. There is no extension allowlist. The default maximum upload size is 10 MiB, configurable by an administrator.

## Inline rendering and safety

Only PNG, JPEG, GIF and WebP render inline. Every other type is sent with a download disposition and a `nosniff` header, so an uploaded HTML, SVG or other active file never executes in the wiki. This is deliberate: attachments are content, not trusted code.

## Search and extraction

Plain UTF-8 `.txt` and `.md` uploads always get cached text extraction, so their content is readable through MCP and by attachment search.

For other document formats (PDF, Word, spreadsheets and similar), set `HMD_TIKA_URL` to an Apache Tika endpoint. With Tika configured, HMD extracts text from those formats and indexes it for keyword and semantic search. Without it, non-text attachments remain ordinary Git-backed files with no indexed content.

## Access control

Attachments follow their page's namespace access policy. Attachments in a public namespace are readable anonymously; attachments in a private namespace require authentication. A missing attachment and a private one return the same result to an anonymous visitor.

## Common pitfalls

- Pasting and dragging only upload images. Use the **attach** button for other file types.
- An upload inserts a link but does not save the page. Save afterwards to commit the page's reference to the file.
- Renaming a page does not move its attachments. The attachment path keeps the slug it was uploaded under.

## Next steps

[[Pages]], [[Markdown And The Editor]], [[MCP Integration]].
