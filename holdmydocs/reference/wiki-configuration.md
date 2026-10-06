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

Edit this file in the dedicated wiki configuration area of `/_/admin`, not in the local instance configuration.
