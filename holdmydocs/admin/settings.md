---
title: Settings And Administration
tags: hmd, administration
---

This page maps the four administration surfaces and where each kind of setting lives.

## Where settings live

| Surface | Route | What it holds |
| --- | --- | --- |
| Personal | `/_/settings` | Appearance, git author identity, and access tokens. |
| Instance | `/_/admin` | Server, git remote, upload limits, users, and configuration export. |
| Namespaces | `/_/namespaces` | Per-namespace visibility, navigation, and page-creation defaults. |
| Wiki | `.wiki.yaml` in the repository | The site name and landing path. |

The three app surfaces all require the `settings` scope, the administrative scope. A user with only `read` and `write` scopes receives 403 on each one.

## Personal settings

`/_/settings` holds everything personal to your account, stored in `users.json`:

- **appearance** — skin, palette, and UI and code fonts. Skins and palettes are per user; see [[Skins And Palettes]]. The top-bar theme control selects System, Light, or Dark separately; that choice is stored in this browser.
- **git author** — your commit identity as `Name <email>`, which overrides the instance default.
- **access tokens** — personal access tokens for API and MCP clients; see [[Personal Access Tokens]].


## Instance settings

`/_/admin` configures the running instance and writes `config.yaml`:

- **server** — bind address and repository directory. Both need a restart.
- **git remote** — remote URL, credentials, default author, and sync mode.
- **behaviour** — maximum upload size and sync poll interval.
- **users** — the bootstrap admin and per-user scopes.
- **environment overrides** — shown when values come from `HMD_*` variables; export writes the current values into `config.yaml`. Exporting any secret variables writes those in plaintext.

The admin UI is covered in detail by [[Configuration]]. A `settings`-scoped account manages user scopes here; scope or password changes revoke that user's active sessions immediately.


## Namespace configuration

`/_/namespaces` lists every namespace and links to its editor. Each namespace has its own visibility (public or private), description, index page, sidebar tree order, skin and palette, quick-create behaviour, and widget set. These are stored in `.namespace.yaml` beside the namespace and are covered on [[Namespaces]].

## Wiki configuration

`.wiki.yaml` sits at the root of the content repository. It holds only content-facing settings — the site name and the landing path — so they travel with the repository to any instance that serves it. They are separate from the local `config.yaml` and are edited in the wiki configuration area of `/_/admin`. See the [[Wiki Configuration Reference]].

## Common pitfalls

- Fields set via `HMD_*` environment variables are read-only on this page and carry a "set via HMD_X" badge. Fields that need a restart carry a "restart reqd" badge.
- The bootstrap admin comes from `HMD_ADMIN_USER` and `HMD_ADMIN_PASSWORD`, used only on the first start; it cannot be changed from the UI.
- Saving the admin form writes `config.yaml` immediately. Prefer keeping secrets out of that file, as the [[Wiki Configuration Reference]] and [[Configuration]] pages explain.

Next: [[Personal Access Tokens]].
