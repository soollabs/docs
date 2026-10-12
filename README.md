# Sool Labs Documentation

Source Markdown for Sool Labs documentation sites.

The documentation is rendered as static HTML by [Hold My Docs](https://github.com/soollabs/holdmydocs).

## Read with HMD

Install [HMD](https://github.com/soollabs/holdmydocs), then run:

```sh
hmd_state="$(mktemp -d)"
HMD_SERVER_BIND=127.0.0.1:8080 \
HMD_APP_DIR="$hmd_state/app" \
HMD_SERVER_REPO_DIR="$hmd_state/repo" \
HMD_SERVER_READ_ONLY=true \
HMD_GIT_REMOTE_URL=https://github.com/soollabs/docs.git \
hmd
```

Open <http://127.0.0.1:8080/holdmydocs/>. HMD fetches the repository for you and serves it read-only.
