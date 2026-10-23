---
title: Git And History
tags: hmd, operations, git
---

HMD saves every change to your pages as a Git commit, so you can see who changed what and bring old versions back from the browser. Nobody has to run Git commands.

## What gets committed

Creating, saving, renaming, moving, tagging, reverting and deleting a page each make one commit. So do attachment uploads and namespace setting changes. The same applies to changes made through the API or MCP.

Saving a page without changing it makes no commit.

## Who is credited

HMD uses the first of these that is set:

1. The person's own **git author** in personal settings, written as `Name <email>`.
2. The default **git author (default)** set by an administrator.
3. The person's username.

A personal access token or MCP client is credited as the user who owns the token.

## Page history

1. Open a page and choose **history**.
2. Select **view** to read an old version, or select two revisions to see what changed between them.
3. Select **revert** to restore a version. The restore is a new commit, so nothing is lost.

History shows the 50 most recent revisions.

A deleted page no longer appears in HMD. Ask an administrator to restore it from the repository's Git history.

## Two people edit the same page

If someone else saves the page while you are editing, HMD refuses your save and keeps your draft. See [[Pages]] for what you can do next.

API and MCP clients get the same refusal. They should read the page again, apply their change to the new content and retry. See [[API Reference]].

HMD never merges commits itself. A Git merge conflict can only come from changes made to the repository outside HMD.

## Sync status

The statusline shows the state of the connection to your remote.

| Statusline | Meaning |
| --- | --- |
| `local only` | No remote is set up. |
| `synced 5m ago` | The last push or fetch worked. |
| `pending` | Commits are waiting to be pushed. |
| `failed` | The last push or fetch failed. |

After fixing the cause of a failure, run **push now** from the command palette. See [[Git Sync]] for modes and credentials.

## Changes made outside HMD

HMD picks up changes to the repository within a few seconds.

| Change | Result |
| --- | --- |
| A commit made in the server's repository | HMD picks it up. |
| A push to the remote, with `bidirectional` sync | HMD pulls it in on its next check. |
| A push to the remote, with `push` sync | HMD does not pull it in, and its own pushes are refused until you merge on the server. |
| Edits to files in the repository folder that are not committed | With `bidirectional` sync, a pull deletes them, including new files. |

Commit your work in the repository folder, or make changes through HMD.

## If sync reports divergent

With `bidirectional` sync, `divergent` means the server and the remote each have commits the other lacks. HMD does not merge them. Saving keeps working on the server in the meantime.

1. Back up the repository folder. See [[Storage And Recovery]].
2. Stop HMD.
3. In the repository folder, run `git fetch origin`, then merge `origin/main` (or your configured branch) and resolve any conflicts.
4. Start HMD and run **push now**.
