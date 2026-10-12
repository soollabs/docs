---
title: Settings And Administration
tags: hmd, administration
---

Every settings section has its own page at `/_/settings/<section>`. This page maps the sections and where each kind of setting lives.

## Where settings live

| Surface | Route | What it holds |
| --- | --- | --- |
| Personal | `/_/settings/appearance` | Appearance, git author identity, and access tokens, each with its own section. |
| Instance | `/_/settings/server` | Server, git remote, upload limits, users, and configuration export, each with its own section. |
| Namespaces | `/_/settings/namespaces` | Per-namespace visibility, navigation, and page-creation defaults. |
| Connected applications | `/_/settings/connections` | Your OAuth connections and disconnection controls. |
| MCP OAuth clients | `/_/settings/oauth-clients` | Administrator-managed client registrations. |
| Wiki | `.wiki.yaml` in the repository | The site name and landing path. |

Personal, instance, namespace and OAuth client administration require the `settings` scope, the administrative scope. Connected applications require a signed-in browser session, not administrative access. A bearer token cannot access either OAuth browser section.

Settings pages share a left-hand navigation with Account and System groups. On narrow screens a compact section selector shows the current section; open it to choose from the grouped links. The selector also works without JavaScript. Connected applications and MCP OAuth clients appear when OAuth is enabled; configuration and environment overrides are under Advanced, which opens automatically when selected.

Individual panels have shareable URLs, such as `/_/settings/git-author` and `/_/settings/users`. Appearance is the default. Panel selection works without JavaScript, although saving personal, instance and namespace settings requires it. Saving keeps the selected section open. The former standalone settings page routes are removed, without redirects.

Namespace pages sit under the Namespaces section: `/_/settings/namespaces/new` and `/_/settings/namespaces/notes/edit`, with export and preview at `/_/settings/namespaces/notes/export` and `/_/settings/namespaces/notes/preview`. Breadcrumbs follow Settings → Namespaces → New namespace or Edit notes.

## Personal settings

The Appearance, Git author and Access tokens sections hold everything personal to your account, stored in `users.json`:

- **appearance** — skin, palette, and UI and code fonts. Skins and palettes are per user; see [[Skins And Palettes]]. The top-bar theme control selects System, Light, or Dark separately; that choice is stored in this browser.
- **git author** — your commit identity as `Name <email>`, which overrides the instance default.
- **access tokens** — personal access tokens for API and MCP clients; see [[Personal Access Tokens]].


## Instance settings

The system sections of `/_/settings` configure the running instance and write `config.yaml`:

- **server** — bind address, repository directory and app data directory. All need a restart.
- **git remote** — remote URL, credentials, default author, and sync mode.
- **behaviour** — maximum upload size and sync poll interval.
- **users** — the bootstrap admin and per-user scopes.
- **config.yaml** — additional instance settings under Advanced.
- **environment overrides** — shown when values come from `HMD_*` variables; export writes the current values into `config.yaml`. Exporting any secret variables writes those in plaintext.

The admin UI is covered in detail by [[Configuration]]. A `settings`-scoped account manages user scopes here; scope or password changes revoke that user's active sessions immediately.


## Namespace configuration

`/_/settings/namespaces` lists every namespace and links to its editor. Each namespace has its own visibility (public or private), description, index page, sidebar tree order, skin and palette, quick-create behaviour, and widget set. These are stored in `.namespace.yaml` beside the namespace and are covered on [[Namespaces]].

## Wiki configuration

`.wiki.yaml` sits at the root of the content repository. It holds only content-facing settings — the site name and the landing path — so they travel with the repository to any instance that serves it. They are separate from the local `config.yaml` and are edited in the wiki configuration area of `/_/settings/behaviour`. See the [[Wiki Configuration Reference]].

## Common pitfalls

- Fields set via `HMD_*` environment variables are read-only on this page and carry a "set via HMD_X" badge. Fields that need a restart carry a "restart reqd" badge.
- The bootstrap admin comes from `HMD_ADMIN_USER` and `HMD_ADMIN_PASSWORD`, used only on the first start; it cannot be changed from the UI.
- Saving the admin form writes `config.yaml` immediately. Prefer keeping secrets out of that file, as the [[Wiki Configuration Reference]] and [[Configuration]] pages explain.

Next: [[Personal Access Tokens]].
