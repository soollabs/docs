---
title: Settings And Administration
tags: hmd, administration
---

Each settings section has its own page at `/_/settings/<section>`. Use the sections below to find your account, instance and namespace settings.

## Where settings live

| Surface | Route | What it holds |
| --- | --- | --- |
| Personal | `/_/settings/appearance` | Appearance, git author identity, and access tokens, each with its own section. |
| Instance | `/_/settings/server` | Server, Git, MCP, OIDC, document search, users and environment overrides, each with its own section. |
| Namespaces | `/_/settings/namespaces` | Per-namespace visibility, navigation, and page-creation defaults. |
| Connected applications | `/_/settings/connections` | Your OAuth connections and disconnection controls. |
| MCP OAuth clients | `/_/settings/oauth-clients` | Administrator-managed client registrations. |
| Wiki | `.wiki.yaml` in the repository | The site name and landing path. |

Personal, instance, namespace and OAuth client administration require the `settings` scope, the administrative scope. Connected applications require a signed-in browser session, not administrative access. A bearer token cannot access either OAuth browser section.

Settings pages share a left-hand navigation with Account and System groups. On narrow screens, open the section selector to choose from the same links. Navigation works without JavaScript. Connected applications and MCP OAuth clients appear when OAuth is enabled; Environment overrides is under Advanced.

Individual panels have shareable URLs, such as `/_/settings/git-author` and `/_/settings/users`. Appearance is the default. Panel selection works without JavaScript, although saving personal, instance and namespace settings requires it. Saving keeps the selected section open.

Namespace pages sit under Namespaces: `/_/settings/namespaces/new` and `/_/settings/namespaces/notes/edit` (General), with `/edit/published`, `/edit/static-site` and `/edit/widgets` for the other panels. Export and preview actions are on the namespace list; the Static site page also offers preview. Breadcrumbs follow Settings → Namespaces → Edit notes → the selected panel.

## Personal settings

The Appearance, Git author and Access tokens sections store your account settings in `users.json`:

- **appearance** — skin, palette, and UI and code fonts. Skins and palettes are per user; see [[Skins And Palettes]]. The top-bar theme control selects System, Light, or Dark separately; that choice is stored in this browser.
- **git author** — your commit identity as `Name <email>`, which overrides the instance default.
- **access tokens** — personal access tokens for API and MCP clients; see [[Personal Access Tokens]].

![Appearance settings in the shared settings navigation](/_/attachments/holdmydocs/admin/settings/appearance.png)

## Instance settings

The system sections of `/_/settings` configure the running instance and write `config.yaml`:

- **server** — bind address, repository directory, origin, proxies, read-only mode, upload limit, default skin and logging.
- **git** — remote URL, user, token file path, default author, branch, sync mode and poll interval.
- **MCP** — MCP and OAuth configuration.
- **OIDC single sign-on** — non-secret identity-provider configuration.
- **document search** — Tika endpoint, model and storage directories.
- **wiki** — site name, landing destination and re-run setup.
- **users** — the bootstrap admin and per-user scopes.
- **environment overrides** — effective `HMD_*` overrides and configuration export. Export writes non-secret file settings only; secrets are never exported.

See [[Configuration]] for instance settings. Changing a user's scopes or password revokes their active sessions immediately.

![Server settings with aligned labels and info icons](/_/attachments/holdmydocs/admin/settings/server.png)

## Namespace configuration

`/_/settings/namespaces` lists every namespace and links to its editor. Each namespace has its own visibility (public or private), description, index page, sidebar tree order, skin and palette, quick-create behaviour, and widget set. These are stored in `.namespace.yaml` beside the namespace and are covered on [[Namespaces]].

![Namespace General settings, including its quick-create template page](/_/attachments/holdmydocs/admin/settings/namespace-general.png)

## Wiki configuration

`.wiki.yaml` stores the site name and landing path at the root of the content repository, so they travel with its pages. Edit it at `/_/settings/wiki`; see [[Wiki Configuration Reference]].

## Common pitfalls

- Fields set via `HMD_*` environment variables are read-only. Each field's info tooltip explains its description, environment override, storage location and restart requirement; restart-required icons use the warning colour.
- The bootstrap admin comes from `HMD_ADMIN_USER` and `HMD_ADMIN_PASSWORD`, used only on the first start; it cannot be changed from the UI.
- Saving writes non-secret settings immediately. Git and OIDC secrets must come from environment variables or private referenced files, never `config.yaml` or UI inputs; see [[Configuration]].
- Turning on `server.read_only` also blocks settings saves. Turn it off in the file or environment and restart; the UI cannot undo it.

Next: [[Personal Access Tokens]].

## Personal Preferences Reference

This table comes from the pinned HMD release's preferences schema. Preferences are stored per account in `users.json` and have no environment overrides.

<!-- generated:preferences -->

| Key | Environment variable | Type and default | Accepted values | Restart | Description |
| --- | --- | --- | --- | --- | --- |
| `skin` | — | string; not specified | `"phosphor"`, `"newsprint"`, `"journal"`, `"soft"`, `"bare"` | — | Typography, spacing, markers and statusline. Widgets and publishing are set per namespace; the same repository works under any skin. |
| `palette` | — | string; not specified | — | — | Colours only, independent of the skin. Swatches follow the current light or dark mode, chosen from the top bar. |
| `font_ui` | — | string; not specified | — | — | Typeface for interface text and page prose. |
| `font_mono` | — | string; not specified | — | — | Typeface for code blocks, the editor and other monospaced text. |
| `git_author` | — | string; not specified | — | — | Your commit identity, as Name &lt;email&gt;. Overrides the instance default author for your saves. |

<!-- /generated:preferences -->
