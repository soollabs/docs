---
title: Wiki Configuration Reference
tags: hmd, reference
---

`.wiki.yaml` sits at the root of the content repository and travels with it:

```yaml
site_name: My Wiki
landing: notes/
```

`site_name` is the application display name. `landing` may name a namespace index such as `notes/` or a page such as `notes/inbox`. When omitted, HMD falls back to the first namespace.

Edit this file at `/_/settings/wiki`, not in the local instance configuration.

<!-- generated:wiki -->

| Key | Environment variable | Type and default | Accepted values | Restart | Description |
| --- | --- | --- | --- | --- | --- |
| `site_name` | — | string; not specified | — | — | Name shown in the top bar, shell prompt, masthead and breadcrumbs. |
| `landing` | — | string; not specified | — | — | Where / opens: a namespace index such as notes/, a page such as notes/inbox, or empty for the first namespace. |

<!-- /generated:wiki -->
