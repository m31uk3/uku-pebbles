# SAGE Documentation Review Notes

## Consistency Check

### Terminology
- **Consistent usage verified:** "memory" (not "record" or "entry") used throughout for the core data unit
- **Consistent usage verified:** "agent" (not "user" or "client") for AI entities
- **Consistent usage verified:** "domain" (not "category" or "topic") for memory classification
- **Consistent usage verified:** "vault" (not "keystore" or "wallet") for encryption management
- **Note:** The binary was renamed from `sage-lite` to `sage-gui` in v3.6; no references to old name found in current code

### Cross-Reference Validity
- All internal package references verified against `internal/` directory structure
- All REST endpoint paths verified against `api/rest/server.go` route registration
- MCP tool names verified against `internal/mcp/tools.go`
- Database table names verified against `deploy/init.sql`
- Protobuf message names verified against `api/proto/sage/v1/tx.proto` and `query.proto`

### Version References
- Current version: v5.0.7 (README.md)
- SDK version: v5.0.8 (`sdk/python/pyproject.toml`) — minor discrepancy, SDK may be released independently
- Go version: 1.24.0 (go.mod)
- CometBFT: v0.38.15 (go.mod)

## Completeness Check

### Documented Components
- [x] ABCI application (13 internal packages)
- [x] REST API (25+ endpoints)
- [x] MCP server (15+ tools)
- [x] Web dashboard (handlers + SPA)
- [x] Python SDK
- [x] Storage layer (BadgerDB, PostgreSQL, SQLite)
- [x] Authentication (Ed25519)
- [x] Encryption (AES-256-GCM)
- [x] Consensus (CometBFT)
- [x] Pre-validation (4 validators)
- [x] PoE engine
- [x] Deployment (Docker Compose)
- [x] Monitoring (Prometheus/Grafana)

### Documentation Gaps

1. **sage-memory/SKILL.md** — Contains a Claude Code skill definition for memory lifecycle management. Not documented as a separate component. This appears to be a Claude Code hook/skill that automates boot/turn/reflect memory operations.

2. **Chrome extension details** — Only high-level structure documented. The extension's `background.js`, `content.js`, and `sage-tools.js` implement tool injection for browser-based AI interfaces, but exact injection targets and supported AI platforms are not enumerated.

3. **sage-launcher process management** — Platform-specific process management (`proc_other.go` for Unix, `proc_windows.go` for Windows) is mentioned but the launchd plist management and Windows service registration are not detailed.

4. **sage-tray (macOS)** — Swift-based system tray application is present but minimal documentation provided. Contains macOS menu bar integration code.

5. **CI/CD pipeline** — `.github/workflows/ci.yml` and `release.yml` exist but their exact steps (build matrix, artifact publishing, Docker push, SDK publishing) are not detailed.

6. **Grafana dashboard details** — Three dashboards exist (`consensus.json`, `poe.json`, `sage-overview.json`) but their specific panels and queries are not documented.

7. **E2E test scenarios** — Four Playwright specs exist but exact test scenarios and assertions are not enumerated.

8. **OpenAPI specification** — `api/openapi.yaml` (29.1KB) provides machine-readable API docs but is not cross-referenced with the human-readable documentation.

9. **Migration logic** — `cmd/sage-gui/migrate.go` and `internal/abci/migrate.go` handle schema and state migrations between versions but migration paths (v3→v4→v5) are not documented.

10. **LevelUp integration** — `integrations/levelup/` appears to be a CTF-specific integration with custom domain tags but the experiment protocol and bridge patterns are not fully documented.

### Language/Framework Limitations

1. **No OpenAPI auto-generation** — REST handlers are manually defined; OpenAPI spec must be manually kept in sync with handler code.

2. **Vanilla JS frontend** — No component framework means limited tooling for static analysis, type checking, or tree-shaking of the dashboard code.

3. **SQLite embedding limitations** — SQLite implementation includes vector storage but lacks the HNSW indexing available in PostgreSQL's pgvector extension. Similarity search may be slower for large datasets in personal mode.

4. **No gRPC endpoint** — Despite protobuf definitions, the API is REST-only. The protobuf is used for on-chain transaction encoding, not as a transport protocol.

## Recommendations

1. Document the `sage-memory/SKILL.md` as part of the Claude Code integration story
2. Add migration path documentation for users upgrading across major versions
3. Consider auto-generating OpenAPI from handler code (or adding handler-to-spec validation)
4. Document the CI/CD pipeline for contributors
