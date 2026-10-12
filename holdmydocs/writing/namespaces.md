---
title: Namespaces
tags: hmd, writing
---

Organise pages into top-level namespaces, each with its own visibility, navigation and appearance.

Every page belongs to exactly one namespace: the first path segment of its slug. In the page address `docs/guides/install`, `docs` is the namespace and `guides` is filing only; the file on disk is `docs/guides/install.md`. Namespaces are never nested; a directory inside a namespace is just an organising folder.

## How a namespace is configured

An optional `.namespace.yaml` in the namespace's directory configures it:

| Key | What it does |
| --- | --- |
| `index` | The page that takes over `/<namespace>/` as the namespace's index page |
| `title`, `description` | Display name and description for the namespace |
| `public` | Whether anonymous visitors can read the whole namespace |
| `widgets` | The sidebar widgets shown for the namespace |
| `skin`, `palette` | Appearance shown to anonymous visitors of a public namespace |
| `new` | The quick-create template: `template` names the hidden template page, `slug` is the slug pattern for new pages |
| `tree` | Preferred ordering of pages in the namespace tree |

The `new` block is what enables `ctrl-j` quick-create. For example, a daily journal namespace might declare:

```yaml
new:
  template: template
  slug: '{{.Now.Format "2006-01-02"}}'
```

Every field is optional. A namespace with no `.namespace.yaml` gets the built-in defaults: the standard widget set, private.

## Manage namespaces

1. Open `/_/settings/namespaces`.

2. Review the rows: name, page count and visibility for every namespace. Click a name to open its index.

3. Choose **Edit** to open General (name, description, index, tree order and quick-create). Use Published, Static site and Widgets in the nested navigation for the other settings. Preview and export actions are on the list; the Static site page also offers preview.

The General page has one **Delete namespace** action. If files exist, the UI asks for confirmation; deletion removes the namespace and every file beneath it, including pages and hidden templates. **Reset namespace settings** removes only `.namespace.yaml`, keeping content.

You can also write `.namespace.yaml` directly into the repository; the running instance picks it up on its next sync. See [[Namespace Configuration Reference]] for the full field reference.

## Public and private namespaces

Visibility is whole-namespace, never per-page. With `public: true`, every page, wiki-link and attachment in the namespace is readable anonymously. A private namespace returns the same result for a missing page and an existing private page, so an anonymous visitor cannot tell the difference.

## Common pitfalls

- Namespace names are single directory names: no slashes, no leading dot. The segments `_` and `attachments` are reserved.
- Setting `public: true` exposes everything in the namespace. Use a separate private namespace for content that must stay internal.

## Next steps

[[Pages]], [[Namespace Configuration Reference]], [[Settings And Administration]].
