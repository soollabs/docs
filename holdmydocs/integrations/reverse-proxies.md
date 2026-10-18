---
title: Reverse Proxies
tags: hmd, integrations, operations
---

Run HMD behind a TLS-terminating proxy (Caddy, Traefik, Nginx Proxy Manager) that keeps the public origin and sends `X-Forwarded-Proto` from a trusted peer.

## Configure HMD

1. Set `server.base_url` to the public origin, for example `https://wiki.example.com`. Scheme and host only: no path, query or fragment. HMD uses it as the browser **Origin** it accepts for cookie-authenticated writes, for MCP upload URLs, the OIDC callback and MCP OAuth. Required when MCP or OIDC is enabled.
2. Set `server.trusted_proxies` to the CIDRs of the peers whose forwarding headers HMD should trust, usually the proxy's own address or network. List only peers you control, never a broad public block. If you control a CDN in front of the proxy, add its ranges too.
3. Restart HMD.

```yaml
server:
  base_url: https://wiki.example.com
  trusted_proxies: ["10.0.0.0/8"]
```

Both settings also have environment-variable equivalents.

## Configure the proxy

- Terminate TLS and send `X-Forwarded-Proto: https`. HMD ignores it from peers not in `server.trusted_proxies`. Without it, HMD treats the connection as plain HTTP: session cookies lack `Secure` and no `Strict-Transport-Security` header is sent.
- Preserve the browser's public **Host** and **Origin** headers. HMD rejects cookie-authenticated writes whose `Origin` differs from `server.base_url`, so a proxy that rewrites either header breaks login, saving and uploads.
- If you use OIDC, register `<base_url>/_/auth/oidc/callback` as the redirect URI and route that path to HMD.

### Caddy

Caddy sets the needed headers automatically:

```caddyfile
wiki.example.com {
    reverse_proxy 127.0.0.1:8080
}
```

Add Caddy's peer address to `server.trusted_proxies`.

### Nginx Proxy Manager

1. Create a proxy host for `wiki.example.com`.
2. Set the forward hostname to `127.0.0.1` (or the machine running HMD) and the forward port to `8080`.
3. Add NPM's peer address to `server.trusted_proxies`.

NPM's default config already sends `Host` and `X-Forwarded-Proto`.

### Traefik

Trust the proxy peer in the entry point and keep `insecure: false`:

```yaml
entryPoints:
  https:
    address: ":8443"
    forwardedHeaders:
      trustedIPs: ["10.0.0.0/8", "127.0.0.1/32"]
      insecure: false
```

Point a router at HMD using this entry point, and list the same network in `server.trusted_proxies`.

## Test

Through the proxy, check login, save, upload and MCP access. Confirm the session cookie is `Secure` and a browser write succeeds.

## Common pitfalls

| Symptom | Cause |
| --- | --- |
| Login works, saves fail | Browser `Origin` does not match `server.base_url`, or the proxy rewrote Host. |
| No HSTS header | HMD did not get an accepted `X-Forwarded-Proto: https`. Add the proxy peer to `server.trusted_proxies`. |
| Path prefix such as `https://example.com/hmd/` | Unsupported. HMD serves from the origin root and rejects a `base_url` with a path. Use a dedicated host. |

## Next steps

- [[Static Export]] for serving a namespace without HMD at all.
- [[MCP Integration]] for reaching HMD over the MCP endpoint.
