---
title: Reverse Proxies
tags: hmd, integrations, operations
---

Put HMD behind a TLS-terminating reverse proxy that preserves the public origin and forwards `X-Forwarded-Proto` from a trusted peer.

## Prerequisites

- A reverse proxy (Nginx Proxy Manager, Traefik, Caddy, or similar) that can terminate TLS and forward the headers below.
- Two HMD settings, both in the config file or their environment-variable equivalents:

  ```yaml
  base_url: https://wiki.example.com
  trusted_proxies: ["10.0.0.0/8"]
  ```

## Configure HMD

1. Set `base_url` to HMD's canonical public origin, for example `https://wiki.example.com`. It must be a bare origin: scheme and host, with no path, query, or fragment. `base_url` is the exact browser **Origin** HMD accepts for cookie-authenticated writes, the origin it uses for MCP attachment-upload capability URLs, the origin it registers for the OIDC callback, and the issuer/resource origin for MCP OAuth. It is required when MCP, OAuth or OIDC is enabled.
2. Set `trusted_proxies` to the CIDRs of the peers HMD should trust for forwarding headers. This is typically the reverse proxy's own address or the network it runs on. List only peers you control, never a broad public block:

   ```yaml
   # In front of HMD directly.
   trusted_proxies: ["10.0.0.0/8"]
   # Behind a CDN you control as the outer hop.
   trusted_proxies: ["10.0.0.0/8", "203.0.113.0/24"]
   ```

3. Restart HMD.

## Configure the proxy

Terminate TLS at the proxy and send `X-Forwarded-Proto: https` to the backend. This is the header HMD uses to detect that the request arrived over TLS. HMD ignores it from every peer not listed in `trusted_proxies`; if the header is missing or ignored, HMD treats the connection as plain HTTP, writes session cookies without `Secure`, and does not send `Strict-Transport-Security`.

Preserve the browser's public **Host** and **Origin** headers. HMD writes the session cookie host-only (no `Domain` attribute) with `SameSite=Lax`, and it rejects cookie-authenticated writes whose `Origin` does not equal `base_url`. A proxy that rewrites either header breaks login, saving, or uploads.

Register `<base_url>/_/auth/oidc/callback` with your identity provider as the redirect URI, and make sure the proxy routes that path to the backend.

### Caddy

Caddy preserves the Host header and sets `X-Forwarded-Proto`, `X-Forwarded-For`, and `X-Forwarded-Host` automatically:

```caddyfile
wiki.example.com {
    reverse_proxy 127.0.0.1:8080
}
```

Add Caddy's peer address to `trusted_proxies`.

### Nginx Proxy Manager (NPM)

Create a proxy host for `wiki.example.com`, set the forward hostname to `127.0.0.1` (or the machine running HMD), and the forward port to `8080`. NPM's default proxy config already sends `Host` and sets `X-Forwarded-Proto` to the incoming scheme, so TLS terminated at NPM reaches HMD as `https`. Add NPM's peer address to `trusted_proxies`.

### Traefik

Define an entry point with `forwardedHeaders`, list the proxy peer under `trustedIPs`, and keep `insecure: false` so Traefik only forwards the `X-Forwarded-*` headers it accepted from a trusted peer:

```yaml
entryPoints:
  https:
    address: ":8443"
    forwardedHeaders:
      trustedIPs: ["10.0.0.0/8", "127.0.0.1/32"]
      insecure: false
```

Point a router at the HMD backend with this entry point, and list that same network in HMD's `trusted_proxies`.

## Test

Test login, save, upload, and MCP access **through the proxy** after changing its configuration. Confirm the session cookie is marked `Secure` and that a cookie-authenticated write from a browser succeeds.

## Common pitfalls

- **Logins work but saves fail.** The browser's `Origin` does not match `base_url`, or the proxy rewrote the Host. Verify both match the public origin exactly.
- **HSTS never appears.** HMD did not receive an accepted `X-Forwarded-Proto: https` — the proxy peer is not in `trusted_proxies`.
- **No path-prefix deployments.** HMD serves from the origin root. A `base_url` with a path is rejected at configuration load, and every route is mounted at the origin root, so a proxy prefix such as `https://example.com/hmd/` needs different reply handling.

## Next steps

- [[Static Export]] for serving a namespace without HMD at all.
- [[MCP Integration]] for reaching HMD over the MCP endpoint.
