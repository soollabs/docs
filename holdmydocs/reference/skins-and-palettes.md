---
title: Skins And Palettes
tags: hmd, reference
---

A skin controls presentation — typography, spacing, borders, markers, and statusline segments. A palette controls colours. Both are per-user choices in `/_/settings` and never change page storage, namespace composition, or the wiki landing path.

## Skins

There are five built-in skins. Each arrives with a paired palette; choosing a skin resets the palette to the pairing unless you pick a palette afterwards.

| Skin | Look | Default palette |
| --- | --- | --- |
| `phosphor` | Terminal green, monospace, `#` markers — the default. | phosphor |
| `newsprint` | Broadsheet — masthead, serif, justified columns, ink on paper. | solarized |
| `journal` | Writing first — serif, wide measure, no chrome. | everforest |
| `soft` | Rounded and low-contrast — warm sans, roomy leading, filled panels. | rosé pine |
| `bare` | Subtraction only — no borders, no markers, wide margins. | one dark |

![A fictional public blog in the newsprint skin, light mode](/_/attachments/holdmydocs/reference/skins-and-palettes/newsprint-light.png)

## Palettes

There are eleven palettes: `phosphor`, `catppuccin`, `dracula`, `everforest`, `gruvbox`, `monokai`, `nord`, `one dark`, `rosé pine`, `solarized`, and `tokyo night`. Each supplies the full colour set for both light and dark mode.


## Light, dark, and system mode

The theme control in the top bar cycles through **System**, **Light**, and **Dark**. System is the default and follows your device's colour preference, including changes while the page is open.

An explicit light or dark choice is remembered in this browser's local storage. Choosing System clears that override. This setting is separate from your account's skin and palette and also applies to anonymous public pages.

## How skin and palette interact

- Choosing a skin resets the palette to the skin's pairing. If you then pick a different palette, that choice is remembered (`palette_explicit`) and the skin stops overriding it.
- Skins and palettes are per user. A namespace's `skin` and `palette` keys in `.namespace.yaml` set what anonymous and public viewers of that namespace see; signed-in users keep their own choices. See [[Namespace Configuration Reference]].
- The install-wide default skin comes from `config.yaml` (`skin` / `HMD_SKIN`); see [[Configuration Reference]].

## Common pitfalls

- A skin change that "loses" your palette is the reset behaviour, not a bug — pick the palette again after the skin.
- The same repository looks different to you and to anonymous visitors when the namespace sets a skin or palette you have overridden for yourself.

Next: [[Limitations]].
