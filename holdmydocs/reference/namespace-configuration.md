---
title: Namespace Configuration Reference
tags: hmd, reference
---

Place `.namespace.yaml` in a namespace directory:

```yaml
title: Documentation
description: Public product documentation
public: true
skin: journal
palette: nord
index: index
tree: [getting-started, guides, reference, about]
widgets: [pages, tags, backlinks]
new:
  template: entry
  slug: '{{.Now.Format "2006-01-02"}}'
```

All keys are optional. `widgets` replaces the default composition rather than adding to it. `public` covers the entire namespace. `index` names the page served at the namespace root and is always first in the tree. `tree` is an optional ordered list of page or folder paths; unlisted siblings follow in alphabetical order. The same tree order is used in the live sidebar and static exports. `new` defines the hidden template and slug pattern used by quick-create.
