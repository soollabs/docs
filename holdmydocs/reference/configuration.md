---
title: Configuration Reference
tags: hmd, reference
---

HMD reads `<HMD_APP_DIR>/config.yaml` by default. `HMD_CONFIG_FILE` chooses a different file. YAML is strict: an unknown key stops startup. Scalar YAML keys have an environment equivalent formed as `HMD_` plus the upper-case path, for example `git.remote_url` becomes `HMD_GIT_REMOTE_URL`; YAML list values do not. Environment values win and are read-only in the admin UI. Restart after changing this file.

| YAML key / environment variable | Type and default | Rules | Secret |
| --- | --- | --- | --- |
| `HMD_APP_DIR` | path, `/data/app` | Private local directory, mode `0700`; not NFS. | No |
| `HMD_CONFIG_FILE` | path | Config file location. | No |
| `HMD_ADMIN_USER` | string | First start only; valid user name. | No |
| `HMD_ADMIN_PASSWORD` | string | First start only; 12-72 bytes, no controls, not a placeholder. | Yes |
| `bind` / `HMD_BIND` | address, `:8080` | Host and port, port 1-65535. | No |
| `repo_dir` / `HMD_REPO_DIR` | path, `/data/repo` | Private writable directory; must not overlap `app_dir` or model storage. | No |
| `max_upload_bytes` / `HMD_MAX_UPLOAD_BYTES` | integer, `10485760` | 1 to 1073741824 bytes. | No |
| `sync_poll_ms` / `HMD_SYNC_POLL_MS` | integer, `10000` | At least 100 ms. | No |
| `sync_mode` / `HMD_SYNC_MODE` | string, `push` | `push` or `bidirectional`. | No |
| `default_branch` / `HMD_DEFAULT_BRANCH` | string, `main` | Valid Git branch name. | No |
| `skin` / `HMD_SKIN` | string, `phosphor` | `phosphor`, `newsprint`, `journal`, `soft`, or `bare`. | No |
| `debug` / `HMD_DEBUG` | boolean, `false` | Enables debug logs. | No |
| `base_url` / `HMD_BASE_URL` | origin | HTTP(S) origin only, without path, query, fragment or user-info. Required for MCP, OAuth or OIDC; its OIDC callback is `/_/auth/oidc/callback`. OAuth requires HTTPS except for explicitly enabled loopback development, and issuer changes require restart. | No |
| `trusted_proxies` | YAML list | CIDRs allowed to set `X-Forwarded-Proto`. | No |
| `git.remote_url` / `HMD_GIT_REMOTE_URL` | HTTPS URL, empty | SSH remotes are unsupported. | No |
| `git.user` / `HMD_GIT_USER` | string, `hmd` | Remote user name. | No |
| `git.token` / `HMD_GIT_TOKEN` | string, empty | Mutually exclusive with `git.token_file`. Prefer a secret file. | Yes |
| `git.token_file` / `HMD_GIT_TOKEN_FILE` | path, empty | Owned regular file, mode at most `0600`, non-empty, at most 64 KiB. | Yes |
| `git.author` / `HMD_GIT_AUTHOR` | string, empty | Optional default `Name <email>` commit identity. | No |
| `mcp.enabled` / `HMD_MCP_ENABLED` | boolean, `false` | Requires `base_url`. | No |
| `oauth.enabled` / `HMD_OAUTH_ENABLED` | boolean, `false` | Enables the MCP OAuth authorisation server; requires `mcp.enabled` and `base_url`. | No |
| `oauth.allow_admin_delegation` / `HMD_OAUTH_ALLOW_ADMIN_DELEGATION` | boolean, `false` | Allows client registrations and users to grant the `settings` scope. This scope is unrestricted across namespaces. | No |
| `oauth.allow_insecure_loopback` / `HMD_OAUTH_ALLOW_INSECURE_LOOPBACK` | boolean, `false` | Development only; permits an HTTP loopback issuer. Do not enable for public deployments. | No |
| `oidc.issuer` / `HMD_OIDC_ISSUER` | HTTPS URL, empty | Enables OIDC; requires the fields below and an admission choice. | No |
| `oidc.client_id` / `HMD_OIDC_CLIENT_ID` | string | Required with issuer. | No |
| `oidc.client_secret` / `HMD_OIDC_CLIENT_SECRET` | string | Mutually exclusive with `client_secret_file`. | Yes |
| `oidc.client_secret_file` / `HMD_OIDC_CLIENT_SECRET_FILE` | path | Same file rules as `git.token_file`. | Yes |
| `oidc.default_scopes` | YAML list, `[read]` | Non-empty subset of `read`, `write`, `settings`. | No |
| `oidc.allowed_subjects` | YAML list | Immutable identity allowlist. Required unless admission is delegated to the identity provider. | No |
| `oidc.allowed_email_domains` | YAML list | Verified email-domain allowlist; no `@`, `/`, or spaces. Required unless admission is delegated to the identity provider. | No |
| `oidc.allow_any_authenticated` / `HMD_OIDC_ALLOW_ANY_AUTHENTICATED` | boolean, `false` | Explicitly delegate admission to the identity provider instead of using an HMD allowlist. | No |
| `oidc.local_login` / `HMD_OIDC_LOCAL_LOGIN` | boolean, `true` | Shows local password login alongside OIDC. | No |
| `oidc.button_text` / `HMD_OIDC_BUTTON_TEXT` | string, `Sign in with SSO` | OIDC button label. | No |
| `oidc.icon` / `HMD_OIDC_ICON` | string, empty | Dashboard Icons name or square SVG path. | No |
| `oidc.allow_insecure_loopback` / `HMD_OIDC_ALLOW_INSECURE_LOOPBACK` | boolean, `false` | Development only; allows HTTP on loopback. | No |
| `document_search.model` / `HMD_DOCUMENT_SEARCH_MODEL` | string, `BAAI/bge-small-en-v1.5` | Hugging Face `owner/model`; must provide compatible 384-dimensional ONNX output. | No |
| `document_search.model_dir` / `HMD_DOCUMENT_SEARCH_MODEL_DIR` | path, `<app>/models` | Must not overlap repository or index storage. | No |
| `document_search.index_dir` / `HMD_DOCUMENT_SEARCH_INDEX_DIR` | path, `<app>/search.bleve` | Derived state; must not overlap repository or model storage. | No |
| `HMD_TIKA_URL` | HTTP(S) URL, empty | Environment only. Private Tika Server with no user-info; one request at a time, 60-second extraction timeout, 8 MiB output limit. | No |

`HMD_TIKA_URL` enables document extraction and semantic attachment search. The default model is pinned and checksum-verified on download. Any other model is operator-supplied and trusted as configuration.

Typical startup errors are actionable: `base_url must be set` means configure the public origin; `unsafe data directory` means recreate or restore a private directory owned by the service user.

Portable site name and landing settings are in repository-tracked `.wiki.yaml`, not `config.yaml`. Namespace visibility and widgets are in each namespace's `.namespace.yaml`. See [[Configuration]] and [[Wiki Configuration Reference]].

## Fixed Limits

The following limits are intentionally fixed. They protect predictable resource use and are not configuration settings:

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
