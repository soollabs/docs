---
title: Wiki Configuration Reference
tags: hmd, reference
---

`.wiki.yaml` sits at the root of the content repository. Edit it at `/_/settings/wiki`.

```yaml
site_name: My Wiki
landing: notes/
```

- `site_name`: the display name of the application.
- `landing`: a namespace index such as `notes/` or a page such as `notes/inbox`. Omitted, it falls back to the first namespace.

<!-- generated:wiki -->

| Key | Environment variable | Type and default | Accepted values | Restart | Description |
| --- | --- | --- | --- | --- | --- |
| `site_name` | — | string; not specified | — | — | Name shown in the top bar, shell prompt, masthead and breadcrumbs. |
| `landing` | — | string; not specified | — | — | Where / opens: a namespace index such as notes/, a page such as notes/inbox, or empty for the first namespace. |

<!-- /generated:wiki -->
