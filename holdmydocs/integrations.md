---
title: Integrations
tags: hmd, integrations
---

Connect HMD to the way you write, host, and publish. None of these integrations is required to create your first wiki.

## Connect an AI assistant

[[MCP Integration]] walks through credentials, the MCP endpoint, and client configuration. Use [[MCP OAuth]] for browser-based authorisation and [[MCP Tool Reference]] for exact tool inputs and outputs. [[LLM Wiki]] shows an example of an assistant-maintained knowledge base.

## Publish a documentation website

[[Static Export]] turns a namespace into a read-only site you can host without HMD. It covers page links, attachments, previewing, and replacing a published snapshot. This documentation site uses that workflow.

## Put the live wiki behind HTTPS

[[Reverse Proxies]] covers TLS termination, the public URL, and trusted proxy headers. Use this when you want people to sign in and work in the live wiki, not just read an export.

## Connect Git or build your own client

- [[Git Sync]] — push content to an HTTPS Git remote or pull external changes.
- [[API Reference]] — use HMD's HTTP API.
- [[Personal Access Tokens]] — limit what a script or integration can access.
