---
title: Settings And Administration
tags: hmd, administration
---

Settings live at `/_/settings/<section>`. Each panel has its own shareable URL, such as `/_/settings/git-author` or `/_/settings/users`; Appearance is the default.

## Where settings live

| Surface | Route | What it holds |
| --- | --- | --- |
| Personal | `/_/settings/appearance` | Appearance, git author identity, access tokens. |
| Instance | `/_/settings/server` | Server, Git, MCP, OIDC, document search, users, environment overrides. |
| Namespaces | `/_/settings/namespaces` | Per-namespace visibility, navigation and page-creation defaults. |
| Connected applications | `/_/settings/connections` | Your OAuth connections and disconnection controls. |
| MCP OAuth clients | `/_/settings/oauth-clients` | Administrator-managed client registrations. |
| Wiki | `.wiki.yaml` in the repository | Site name and landing path. |

- Personal, instance, namespace and OAuth client settings need the `settings` (administrative) scope.
- Connected applications need a signed-in browser session, not administrative access. A bearer token cannot access either OAuth browser section.
- Connected applications and MCP OAuth clients appear only when OAuth is enabled. Environment overrides is under Advanced.
- Navigation and panel selection work without JavaScript. Saving needs it, and keeps the selected section open.

## Personal settings

These sections store your account settings in `users.json`:

- **Appearance**: skin, palette, and UI and code fonts; see [[Skins And Palettes]]. The top-bar theme control (System, Light, Dark) is stored in this browser.
- **Git author**: your commit identity as `Name <email>`, which overrides the instance default.
- **Access tokens**: personal access tokens for API and MCP clients; see [[Personal Access Tokens]].

![Skin and palette choices in the appearance settings](/_/attachments/holdmydocs/admin/settings/appearance.png)

## Instance settings

The system sections write `config.yaml`; see [[Configuration]].

- **Server**: bind address, repository directory, origin, proxies, read-only mode, upload limit, default skin, logging.
- **Git**: remote URL, user, token file path, default author, branch, sync mode, poll interval.
- **MCP**: MCP and OAuth configuration.
- **OIDC single sign-on**: non-secret identity-provider configuration.
- **Document search**: Tika endpoint, model and storage directories.
- **Wiki**: site name, landing destination, re-run setup.
- **Users**: the bootstrap admin and per-user scopes. Changing a user's scopes or password revokes their active sessions immediately.
- **Environment overrides**: effective `HMD_*` overrides and configuration export. Export writes non-secret file settings only.

![Server settings with info icons](/_/attachments/holdmydocs/admin/settings/server.png)

## Namespace configuration

`/_/settings/namespaces` lists every namespace and links to its editor. Each namespace has visibility (public or private), description, index page, sidebar tree order, skin and palette, quick-create behaviour and widget set, stored in `.namespace.yaml`. See [[Namespaces]].

- New namespace: `/_/settings/namespaces/new`.
- Editor: `/_/settings/namespaces/notes/edit` (General), plus `/edit/published`, `/edit/static-site` and `/edit/widgets`.
- Export and preview actions are on the namespace list; the Static site page also offers preview.

![Namespace General settings, including its quick-create template page](/_/attachments/holdmydocs/admin/settings/namespace-general.png)

## Wiki configuration

`.wiki.yaml` at the root of the content repository stores the site name and landing path. Edit it at `/_/settings/wiki`; see [[Wiki Configuration Reference]].

## Common pitfalls

- Fields set via `HMD_*` environment variables are read-only. Each field's info tooltip shows its environment override, storage location and restart requirement.
- The bootstrap admin comes from `HMD_ADMIN_USER` and `HMD_ADMIN_PASSWORD`, used only on the first start. It cannot be changed from the UI.
- Git and OIDC secrets must come from environment variables or private referenced files, never `config.yaml` or UI inputs; see [[Configuration]].
- Read-only mode (`HMD_SERVER_READ_ONLY`) makes settings view-only. Unset it and restart to change them.
- Settings that need a restart keep their running value until HMD restarts. A banner lists them, with a **Shut down** button that stops HMD so its supervisor can start it again.

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
