---
title: Namespaces
tags: hmd, writing
---

Namespaces are top-level groups of pages, each with its own visibility, navigation and appearance.

Every page belongs to exactly one namespace: the first path segment of its slug. In `docs/guides/install`, `docs` is the namespace and `guides` is a folder (the file is `docs/guides/install.md`). Namespaces do not nest.

## Configure a namespace

Add an optional `.namespace.yaml` to the namespace's directory. Every key is optional. Without the file, the namespace is private with the standard widget set.

| Key | What it does |
| --- | --- |
| `index` | The page that takes over `/<namespace>/` |
| `title`, `description` | Display name and description |
| `public` | Whether anonymous visitors can read the whole namespace |
| `widgets` | Sidebar widgets for the namespace |
| `skin`, `palette` | Appearance shown to anonymous visitors of a public namespace |
| `new` | Quick-create: `template` names the hidden template page, `slug` is the slug pattern for new pages |
| `tree` | Preferred page order in the namespace tree |

The `new` block enables `ctrl-j` quick-create. For example, a daily journal:

```yaml
new:
  template: template
  slug: '{{.Now.Format "2006-01-02"}}'
```

See [[Namespace Configuration Reference]] for every field. If you write `.namespace.yaml` into the repository directly, the instance picks it up on its next sync.

## Manage namespaces

1. Open `/_/settings/namespaces`. Each row shows name, page count and visibility; click a name to open its index.
2. Choose **Edit** for General (name, description, index, tree order, quick-create). Published, Static site and Widgets are in the nested navigation.
3. Use **Reset namespace settings** to remove only `.namespace.yaml` and keep content.
4. Use **Delete namespace** to remove the namespace and every file beneath it, including pages and hidden templates. The UI asks for confirmation if files exist.

## Public and private

Visibility applies to the whole namespace, never per page. With `public: true`, every page, wiki-link and attachment in it is readable anonymously, so keep internal content in a separate private namespace. A private namespace gives anonymous visitors the same response for a missing page and an existing one.

Namespace names are single directory names: no slashes, no leading dot. `_` and `attachments` are reserved.

## Next steps

[[Pages]], [[Namespace Configuration Reference]], [[Settings And Administration]].
