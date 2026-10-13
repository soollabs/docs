---
title: Configuration Reference
tags: hmd, reference
---

HMD reads `<HMD_APP_DIR>/config.yaml` by default. `HMD_CONFIG_FILE` chooses a different file. Unknown YAML keys stop startup.

Scalar keys normally have an environment equivalent formed as `HMD_` plus the upper-case dotted path with underscores; lists do not. Environment values override file values and make their settings controls read-only.

The table comes from the pinned HMD release's settings schema. Its Restart column describes changes saved through the UI. Restart HMD after editing the file outside the application.

<!-- generated:config -->

| Key | Environment variable | Type and default | Accepted values | Restart | Description |
| --- | --- | --- | --- | --- | --- |
| `server.bind` | `HMD_SERVER_BIND` | string, `":8080"` | format: `"host-port"` | Yes | Address and port HMD listens on, in host:port form. Use 127.0.0.1:8080 to accept connections from this computer only. |
| `server.repo_dir` | `HMD_SERVER_REPO_DIR` | string, `"/data/repo"` | — | Yes | Private directory holding the Git repository of pages, attachments and wiki configuration. Must not overlap the app directory. |
| `server.app_dir` (environment only; not a file key) | `HMD_APP_DIR` | string; not specified | — | Yes | Private application state directory; defaults to /data/app. |
| `server.config_file` (environment only; not a file key) | `HMD_CONFIG_FILE` | string; not specified | — | Yes | Path to the YAML configuration file; overrides the default location in the app directory. |
| `server.base_url` | `HMD_SERVER_BASE_URL` | string, `""` | format: `"origin"`; schemes: `"http"`, `"https"` | Yes | Public origin of HMD, such as https://wiki.example.com, with no path. Browser writes must come from this origin; MCP upload links and the OIDC callback use it. Required for MCP and OIDC. |
| `server.trusted_proxies` | — | array, `[]` | items: string; format: `"cidr"` | Yes | CIDR ranges of reverse proxies allowed to set X-Forwarded-Proto. List only proxies you control. |
| `server.read_only` (environment only; not a file key) | `HMD_SERVER_READ_ONLY` | boolean, `false` | — | Yes | Serve the wiki without allowing edits, uploads, setup, administrator operations, settings changes or pushes. Set only in the environment, so the settings screen cannot switch it on and leave no way back. |
| `server.debug` | `HMD_SERVER_DEBUG` | boolean, `false` | — | Yes | Log at debug level. Logs never include credentials, queries or page bodies. |
| `server.max_upload_bytes` | `HMD_SERVER_MAX_UPLOAD_BYTES` | integer, `10485760` | minimum: `1`; maximum: `1073741824` | No | Largest attachment upload accepted, in bytes (default 10 MiB). |
| `server.tika_timeout` | `HMD_SERVER_TIKA_TIMEOUT` | integer, `120` | minimum: `0`; maximum: `3600` | Yes | How long startup waits for Tika to be available before failing. 0 checks once. |
| `server.skin` | `HMD_SERVER_SKIN` | string, `"phosphor"` | `"phosphor"`, `"newsprint"`, `"journal"`, `"soft"`, `"bare"` | No | Skin used for users who have not chosen their own. |
| `server.admin.user` (environment only; not a file key) | `HMD_ADMIN_USER` | string; not specified | — | No | Bootstrap administrator user name, managed from the environment rather than config.yaml. |
| `server.admin.password` (environment only; not a file key) | `HMD_ADMIN_PASSWORD` | string; not specified | — | No | Bootstrap administrator password, managed from the environment rather than config.yaml. **Secret.** |
| `git.remote_url` | `HMD_GIT_REMOTE_URL` | string, `""` | format: `"url"`; schemes: `"https"` | No | HTTPS URL of an optional Git remote to push to. Leave empty to keep the repository local only. |
| `git.user` | `HMD_GIT_USER` | string, `"hmd"` | — | No | User name sent to the Git remote when authenticating. |
| `git.author` | `HMD_GIT_AUTHOR` | string, `""` | — | No | Commit author, as Name &lt;email&gt;, for users who have not set a personal Git author. |
| `git.token_file` | `HMD_GIT_TOKEN_FILE` | string, `""` | — | No | Path to a private file (mode 0600 or stricter) containing the Git remote token. |
| `git.token` (environment only; not a file key) | `HMD_GIT_TOKEN` | string; not specified | — | No | Personal access token for the Git remote. **Secret.** |
| `git.branch` | `HMD_GIT_BRANCH` | string, `"main"` | format: `"git-branch"` | No | Git branch that HMD commits to and pushes. |
| `git.sync_mode` | `HMD_GIT_SYNC_MODE` | string, `"push"` | `"push"` (push (local → remote only)); `"bidirectional"` (bidirectional (fetch + fast-forward pull)) | No | push sends local commits to the remote only. bidirectional also fetches and fast-forwards remote changes; divergent histories fail rather than merge. |
| `git.sync_poll_ms` | `HMD_GIT_SYNC_POLL_MS` | integer, `10000` | minimum: `100` | No | Interval in milliseconds between browser sync-status checks; in read-only mode also the background fetch interval, which is fixed at startup. |
| `mcp.enabled` | `HMD_MCP_ENABLED` | boolean, `false` | — | Yes | Serve the MCP endpoint at /_/mcp so AI assistants can use the wiki with a personal access token. Requires server.base_url. |
| `mcp.oauth.enabled` | `HMD_MCP_OAUTH_ENABLED` | boolean, `false` | — | Yes | Let MCP clients sign in with OAuth instead of a pasted token. Requires MCP and an https server.base_url; http is allowed only on loopback with insecure loopback enabled. |
| `mcp.oauth.dynamic_registration` | `HMD_MCP_OAUTH_DYNAMIC_REGISTRATION` | boolean, `false` | — | Yes | Let MCP clients register themselves. When off, an administrator registers each client under MCP OAuth clients. |
| `mcp.oauth.allow_insecure_loopback` | `HMD_MCP_OAUTH_ALLOW_INSECURE_LOOPBACK` | boolean, `false` | — | Yes | Development only: permit http OAuth origins on loopback addresses. |
| `mcp.oauth.allow_admin_delegation` | `HMD_MCP_OAUTH_ALLOW_ADMIN_DELEGATION` | boolean, `false` | — | Yes | Allow an administrator to grant a client the settings scope during OAuth consent. |
| `oidc.issuer` | `HMD_OIDC_ISSUER` | string, `""` | format: `"url"`; schemes: `"https"`, `"http"` | Yes | HTTPS issuer URL of the OpenID Connect provider. Setting it enables single sign-on; register &lt;base_url&gt;/_/auth/oidc/callback with the provider. |
| `oidc.client_id` | `HMD_OIDC_CLIENT_ID` | string, `""` | — | Yes | Client ID issued by the identity provider. |
| `oidc.client_secret_file` | `HMD_OIDC_CLIENT_SECRET_FILE` | string, `""` | — | Yes | Path to a private file (mode 0600 or stricter) containing the OIDC client secret. |
| `oidc.client_secret` (environment only; not a file key) | `HMD_OIDC_CLIENT_SECRET` | string; not specified | — | Yes | Client secret issued by the identity provider. **Secret.** |
| `oidc.local_login` | `HMD_OIDC_LOCAL_LOGIN` | boolean, `true` | — | Yes | Keep the username and password form alongside single sign-on. Useful as a fallback if the provider is unavailable. |
| `oidc.button_text` | `HMD_OIDC_BUTTON_TEXT` | string, `"Sign in with SSO"` | — | Yes | Label of the single sign-on login button. |
| `oidc.icon` | `HMD_OIDC_ICON` | string, `""` | — | Yes | Dashboard Icons name, or path to a square SVG, shown on the login button. |
| `oidc.default_scopes` | — | array, `["read"]` | items: string; `"read"`, `"write"`, `"settings"` | Yes | Scopes given to a user the first time they sign in with OIDC: any of read, write and settings. |
| `oidc.allowed_subjects` | — | array, `[]` | items: string | Yes | Provider subject IDs allowed to sign in. Required unless email domains or any authenticated identity are allowed. |
| `oidc.allowed_email_domains` | — | array, `[]` | items: string; pattern: `"^[^@/\\s]+$"` | Yes | Email domains, such as example.com, whose verified addresses may sign in. |
| `oidc.allow_any_authenticated` | `HMD_OIDC_ALLOW_ANY_AUTHENTICATED` | boolean, `false` | — | Yes | Admit anyone the identity provider authenticates, instead of using an HMD allowlist. |
| `oidc.allow_insecure_loopback` | `HMD_OIDC_ALLOW_INSECURE_LOOPBACK` | boolean, `false` | — | Yes | Development only: permit an http issuer on loopback addresses. |
| `document_search.tika_url` | `HMD_DOCUMENT_SEARCH_TIKA_URL` | string; not specified | format: `"url"`; schemes: `"http"`, `"https"` | Yes | URL of a private Apache Tika server, such as http://tika:9998, used to extract text from PDF and Office attachments for search. Leave empty to turn document extraction off; HMD checks the server at startup. |
| `document_search.model` | `HMD_DOCUMENT_SEARCH_MODEL` | string, `"BAAI/bge-small-en-v1.5"` | pattern: `"^[^\\/\\s]+\\/[^\\/\\s]+$"` | Yes | Hugging Face model, as owner/model, used for semantic attachment search. Must produce 384-dimensional ONNX output. |
| `document_search.model_dir` | `HMD_DOCUMENT_SEARCH_MODEL_DIR` | string; not specified | — | Yes | Directory holding the embedding model; defaults to models under the app directory. |
| `document_search.index_dir` | `HMD_DOCUMENT_SEARCH_INDEX_DIR` | string, `""` | — | Yes | Directory holding the document search index. |

<!-- /generated:config -->

`document_search.tika_url` (or `HMD_DOCUMENT_SEARCH_TIKA_URL`) enables document extraction and semantic attachment search. The default model is pinned and checksum-verified on download. Any other model is operator-supplied and trusted as configuration.

MCP and OIDC require `server.base_url`, the public origin. An `unsafe data directory` error means recreate or restore a private directory owned by the service user.

MCP OAuth uses `server.base_url` as its issuer and resource origin. HTTPS is required unless `mcp.oauth.allow_insecure_loopback` explicitly permits local development. OAuth settings and issuer changes require a restart; live issuer changes are rejected while OAuth is enabled. Dynamic registration allows five attempts per minute globally and at most 32 dynamic registrations. See [[MCP OAuth]].

Environment-only rows are not `config.yaml` keys. Git tokens and OIDC client secrets must come from the environment or a private referenced file; exporting configuration never includes secrets. See [[Configuration]] and [[Upgrade HMD]].

Portable site name and landing settings are in repository-tracked `.wiki.yaml`, not `config.yaml`. Namespace visibility and widgets are in each namespace's `.namespace.yaml`. See [[Configuration]] and [[Wiki Configuration Reference]].

## Fixed Limits

These limits are fixed and cannot be changed in configuration:

| Resource | Limit |
| --- | --- |
| Ordinary form request | 2 MiB |
| Markdown body | 1 MiB |
| Stored Markdown page | 1 MiB plus 64 KiB frontmatter allowance |
| Page title, namespace title, Git author | 256 runes |
| Tags | 32 per page, 64 runes each |
| Search query | 512 runes |
| Extracted attachment text | 8 MiB |
| Concurrent attachment semantic searches | 2 |
| Concurrent namespace exports | 1 |
| Namespace export source data | 10,000 files and 100 MiB |
