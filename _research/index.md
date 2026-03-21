# SAGE Codebase Documentation Index

> **AI Instructions:** This documentation set describes the SAGE (Sovereign Agent Governed Experience) codebase — a persistent, consensus-validated memory infrastructure for AI agents. Start with this file for navigation, then read specific documents as needed.

## Quick Reference

| Question | Document |
|----------|----------|
| What is SAGE and how is it structured? | [architecture.md](architecture.md) |
| What packages/modules exist? | [components.md](components.md) |
| What APIs and endpoints exist? | [interfaces.md](interfaces.md) |
| What data is stored and how? | [data_models.md](data_models.md) |
| How do key processes work? | [workflows.md](workflows.md) |
| What dependencies does the project use? | [dependencies.md](dependencies.md) |
| What is the file/directory layout? | [codebase_info.md](codebase_info.md) |
| What gaps or inconsistencies exist? | [review_notes.md](review_notes.md) |

## Table of Contents

### [architecture.md](architecture.md)
System architecture overview, layer descriptions, design patterns (ABCI consensus, two-store model, PoE weighting, RBAC gates), and key design decisions with rationale. Includes Mermaid diagrams.

### [components.md](components.md)
Detailed breakdown of all 13 internal packages, 4 binary entrypoints, REST API server, web dashboard, Python SDK, browser extension, and deployment infrastructure. Per-component: purpose, location, key files, dependencies, interfaces.

### [interfaces.md](interfaces.md)
Complete API reference: 25+ REST endpoints with request/response formats, 15+ MCP tools with parameters, Python SDK methods, internal Go interfaces (`MemoryStore`, `OffchainStore`, `AccessStore`, `OrgStore`, `AgentStore`), and authentication scheme (Ed25519 signatures).

### [data_models.md](data_models.md)
ER diagram, memory record schema, all 19 database tables (PostgreSQL/SQLite), BadgerDB key-value structure, protobuf transaction types, clearance levels, and encryption format.

### [workflows.md](workflows.md)
Step-by-step breakdowns of: memory submission pipeline, consensus voting, RBAC access control, vault encryption lifecycle, agent registration, LAN pairing, network redeployment, MCP tool execution, and dashboard SSE events.

### [dependencies.md](dependencies.md)
Auto-extracted dependency report: Go modules (CometBFT, chi, pgx, badger, zerolog), Python SDK (httpx, pydantic, PyNaCl), Node.js (Playwright for E2E).

### [codebase_info.md](codebase_info.md)
Auto-generated directory tree (depth 4), file type statistics (252 files, 66 directories), and project type detection.

### [review_notes.md](review_notes.md)
Consistency check findings and documentation gap analysis.

## Codebase Overview

**SAGE** gives AI agents institutional memory that persists across conversations, goes through BFT consensus validation, carries confidence scores, and decays over time. Built on CometBFT v0.38 consensus primitives.

**Key stats:**
- **Language:** Go 1.24 (backend), Vanilla JS (frontend), Python (SDK)
- **Total files:** 252 (115 `.go`, 30 `.py`, 25 `.js`)
- **Core packages:** 13 internal Go packages
- **Binaries:** 4 (`amid`, `sage-gui`, `sage-cli`, `sage-launcher`)
- **Stack:** Go / CometBFT v0.38 / chi / SQLite+PostgreSQL / BadgerDB / Ed25519 + AES-256-GCM + Argon2id / MCP
- **License:** Apache 2.0 (code), CC BY 4.0 (papers)

**Deployment modes:**
1. **Personal** — `sage-gui serve` (single CometBFT node, SQLite, 4 in-process validators)
2. **Multi-agent network** — Docker Compose (4 CometBFT nodes, PostgreSQL + pgvector, Prometheus/Grafana)
3. **MCP server** — `sage-gui mcp` (stdio JSON-RPC for Claude Desktop, ChatGPT, etc.)
