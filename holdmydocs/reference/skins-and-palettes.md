---
title: Skins And Palettes
tags: hmd, reference
---

A skin sets presentation (typography, spacing, borders, markers, statusline segments). A palette sets colours. Both are per-user choices in `/_/settings` and never change page storage, namespace composition, or the wiki landing path.

## Skins

Choosing a skin resets the palette to its pairing unless you pick a palette afterwards.

| Skin | Look | Default palette |
| --- | --- | --- |
| `phosphor` | Terminal green, monospace, `#` markers; the page title types itself in and links invert on hover. The default. | phosphor |
| `newsprint` | Broadsheet: a centred masthead between double rules, serif, justified columns, an italic lede with a drop cap. | solarized |
| `journal` | Writing first: serif, paper grain, ruled lines with a margin line, blockquotes as side notes, taped images. | everforest |
| `soft` | Rounded and low-contrast: warm sans, a floating top bar, window dots on code blocks, callout cards. | rosé pine |
| `bare` | No borders, wide margins, a large tight title with faint section numbers. | one dark |

The phosphor title animation is skipped when the device asks for reduced motion.

![A fictional public blog in the newsprint skin, light mode](/_/attachments/holdmydocs/reference/skins-and-palettes/newsprint-light.png)

## Palettes

Eleven palettes, each with light and dark variants: `phosphor`, `catppuccin`, `dracula`, `everforest`, `gruvbox`, `monokai`, `nord`, `one dark`, `rosé pine`, `solarized`, `tokyo night`.

## Light, dark, and system mode

The theme control in the top bar cycles **System**, **Light**, **Dark**. System is the default and follows your device, including live changes.

An explicit light or dark choice is kept in this browser's local storage; choosing System clears it. It is separate from your skin and palette and also applies to anonymous public pages.

## How skin and palette interact

- Picking a palette after a skin is remembered (`palette_explicit`), and the skin stops overriding it. If a skin change "loses" your palette, pick the palette again.
- A namespace's `skin` and `palette` keys in `.namespace.yaml` set what anonymous and public viewers see. Signed-in users keep their own choices, so you may see a different look from anonymous visitors. See [[Namespace Configuration Reference]].
- The install-wide default skin is `server.skin` / `HMD_SERVER_SKIN` in `config.yaml`; see [[Configuration Reference]].

Next: [[Limitations]].
