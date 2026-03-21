# Codebase Structure Analysis

## Project Types Detected
Go, Python, Docker Compose, Docker, Make-based, Node.js/JavaScript

## Statistics
- Total files: 252
- Total directories: 66
- Analysis depth: 4

## Top File Types
- .go: 115
- .py: 30
- .js: 25
- .md: 11
- .png: 10
- .json: 9
- .sh: 8
- .yml: 6
- .html: 6
- .yaml: 4

## Key Directories
- .
- sdk/python

## Directory Tree

```
sage/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── api/
│   ├── proto/
│   │   └── sage/
│   │       └── v1/
│   │           ├── buf.gen.yaml
│   │           ├── buf.yaml
│   │           ├── query.proto
│   │           └── tx.proto
│   ├── rest/
│   │   ├── middleware/
│   │   │   ├── auth.go
│   │   │   ├── logging.go
│   │   │   ├── middleware_test.go
│   │   │   ├── problem.go
│   │   │   └── ratelimit.go
│   │   ├── access_handler.go
│   │   ├── agent_handler.go
│   │   ├── dept_handler.go
│   │   ├── embed_handler.go
│   │   ├── handlers_test.go
│   │   ├── helpers.go
│   │   ├── memory_handler.go
│   │   ├── org_handler.go
│   │   ├── pipe_handler.go
│   │   ├── server.go
│   │   └── vote_handler.go
│   └── openapi.yaml
├── cmd/
│   ├── amid/
│   │   └── main.go
│   ├── sage-cli/
│   │   └── main.go
│   ├── sage-gui/
│   │   ├── config.go
│   │   ├── config_test.go
│   │   ├── main.go
│   │   ├── mcp.go
│   │   ├── mcp_test.go
│   │   ├── migrate.go
│   │   ├── migrate_test.go
│   │   ├── node.go
│   │   ├── node_controller.go
│   │   ├── quorum.go
│   │   ├── seed.go
│   │   ├── vault.go
│   │   └── wizard.go
│   ├── sage-launcher/
│   │   ├── main.go
│   │   ├── main_test.go
│   │   ├── proc_other.go
│   │   └── proc_windows.go
│   └── sage-tray/
│       └── main.swift
├── deploy/
│   ├── monitoring/
│   │   ├── grafana/
│   │   │   ├── dashboards/
│   │   │   │   ├── consensus.json
│   │   │   │   ├── poe.json
│   │   │   │   └── sage-overview.json
│   │   │   └── provisioning/
│   │   │       ├── dashboards/
│   │   │       │   └── ... (max depth reached)
│   │   │       └── datasources/
│   │   │           └── ... (max depth reached)
│   │   ├── alerts.yml
│   │   └── prometheus.yml
│   ├── scripts/
│   │   ├── backup-cometbft.sh
│   │   └── backup-postgres.sh
│   ├── docker-compose.monitoring.yml
│   ├── docker-compose.yml
│   ├── Dockerfile.abci
│   ├── Dockerfile.node
│   ├── init-testnet.sh
│   └── init.sql
├── docs/
│   ├── ARCHITECTURE.md
│   ├── connect.html
│   ├── favicon.svg
│   ├── GETTING_STARTED.md
│   ├── index.html
│   ├── og-image.png
│   ├── privacy.html
│   ├── sage-brain.svg
│   ├── screen-brain.png
│   ├── screen-config.png
│   ├── screen-network.png
│   ├── screen-overview.png
│   ├── screen-security.png
│   └── screen-update.png
├── e2e/
│   ├── agent-identity.spec.js
│   ├── bulk-operations.spec.js
│   ├── dashboard.spec.js
│   └── network.spec.js
├── extension/
│   ├── chrome/
│   │   ├── icons/
│   │   │   ├── generate-icons.html
│   │   │   ├── generate-icons.js
│   │   │   ├── icon128.png
│   │   │   ├── icon16.png
│   │   │   └── icon48.png
│   │   ├── background.js
│   │   ├── content.css
│   │   ├── content.js
│   │   ├── manifest.json
│   │   ├── popup.css
│   │   ├── popup.html
│   │   ├── popup.js
│   │   ├── README.md
│   │   └── sage-tools.js
│   ├── build.sh
│   ├── manifest.firefox.json
│   └── store-listing.md
├── installer/
│   ├── linux/
│   │   ├── build-linux.sh
│   │   ├── install.sh
│   │   └── sage.desktop
│   ├── macos/
│   │   ├── AppIcon.icns
│   │   └── build-dmg.sh
│   ├── windows/
│   │   ├── build-exe.sh
│   │   ├── sage-installer.nsi
│   │   └── sage.ico
│   └── icon.svg
├── integrations/
│   └── levelup/
│       ├── experiment_protocol.py
│       └── sage_bridge.py
├── internal/
│   ├── abci/
│   │   ├── app.go
│   │   ├── app_test.go
│   │   ├── migrate.go
│   │   ├── state.go
│   │   └── state_test.go
│   ├── appvalidator/
│   │   ├── manager.go
│   │   ├── manager_test.go
│   │   ├── validator.go
│   │   └── validator_test.go
│   ├── auth/
│   │   ├── ed25519.go
│   │   └── ed25519_test.go
│   ├── embedding/
│   │   ├── hash.go
│   │   ├── ollama.go
│   │   ├── provider.go
│   │   └── provider_test.go
│   ├── mcp/
│   │   ├── server.go
│   │   ├── server_test.go
│   │   ├── tools.go
│   │   └── tools_test.go
│   ├── memory/
│   │   ├── cleanup.go
│   │   ├── confidence.go
│   │   ├── lifecycle.go
│   │   ├── lifecycle_test.go
│   │   ├── model.go
│   │   └── validation.go
│   ├── metrics/
│   │   ├── health.go
│   │   ├── metrics.go
│   │   └── server.go
│   ├── orchestrator/
│   │   ├── backup.go
│   │   ├── bundle.go
│   │   ├── redeployer.go
│   │   └── redeployer_test.go
│   ├── poe/
│   │   ├── collusion.go
│   │   ├── domain.go
│   │   ├── engine.go
│   │   ├── engine_test.go
│   │   ├── epoch.go
│   │   ├── ewma.go
│   │   └── types.go
│   ├── store/
│   │   ├── badger.go
│   │   ├── pipeline_test.go
│   │   ├── postgres.go
│   │   ├── postgres_test.go
│   │   ├── sqlite.go
│   │   ├── sqlite_test.go
│   │   └── store.go
│   ├── tx/
│   │   ├── codec.go
│   │   ├── codec_test.go
│   │   └── types.go
│   ├── validator/
│   │   ├── manager.go
│   │   ├── manager_test.go
│   │   └── quorum.go
│   └── vault/
│       ├── vault.go
│       └── vault_test.go
├── papers/
│   ├── Paper1 - Agent Memory Infrastructure - Byzantine-Resilient Institutional Memory for Multi-Agent Systems.pdf
│   ├── Paper2 - Consensus-Validated Memory Improves Agent Performance on Complex Tasks.pdf
│   ├── Paper3 - Institutional Memory as Organizational Knowledge - AI Agents That Learn Their Jobs from Experience Not Instructions.pdf
│   ├── Paper4 - Longitudinal Learning in Governed Multi-Agent Systems - How Institutional Memory Improves Agent Performance Over Time.pdf
│   └── README.md
├── sage-memory/
│   └── SKILL.md
├── scripts/
│   └── setup_studio_org.py
├── sdk/
│   └── python/
│       ├── examples/
│       │   ├── __init__.py
│       │   ├── async_example.py
│       │   ├── complete_walkthrough.py
│       │   ├── federation.py
│       │   ├── full_lifecycle.py
│       │   ├── multi_agent.py
│       │   ├── org_setup.py
│       │   ├── quickstart.py
│       │   ├── rbac_clearance.py
│       │   └── sage_bridge_example.py
│       ├── src/
│       │   └── sage_sdk/
│       │       ├── __init__.py
│       │       ├── async_client.py
│       │       ├── auth.py
│       │       ├── client.py
│       │       ├── exceptions.py
│       │       └── models.py
│       ├── tests/
│       │   ├── __init__.py
│       │   ├── conftest.py
│       │   ├── test_async_client.py
│       │   ├── test_auth.py
│       │   ├── test_client.py
│       │   ├── test_dept_rbac.py
│       │   ├── test_models.py
│       │   └── test_org_federation.py
│       ├── pyproject.toml
│       └── README.md
├── test/
│   ├── benchmark/
│   │   ├── config.json
│   │   ├── load.js
│   │   ├── load_test.py
│   │   └── query.js
│   ├── byzantine/
│   │   ├── fault_test.go
│   │   └── helpers_test.go
│   └── integration/
│       ├── consensus_proof_test.go
│       ├── cross_node_test.py
│       ├── dept_rbac_test.go
│       ├── federation_acl_test.py
│       ├── helpers_test.go
│       ├── memory_lifecycle_test.go
│       └── poe_test.go
├── web/
│   ├── static/
│   │   ├── css/
│   │   │   └── sage.css
│   │   ├── js/
│   │   │   ├── components/
│   │   │   │   ├── confidence-badge.js
│   │   │   │   ├── domain-filter.js
│   │   │   │   ├── memory-card.js
│   │   │   │   ├── search-bar.js
│   │   │   │   ├── stats-panel.js
│   │   │   │   └── timeline-bar.js
│   │   │   ├── pages/
│   │   │   │   ├── brain.js
│   │   │   │   ├── memory-detail.js
│   │   │   │   ├── search.js
│   │   │   │   └── settings.js
│   │   │   ├── api.js
│   │   │   ├── app.js
│   │   │   └── sse.js
│   │   ├── favicon.svg
│   │   └── index.html
│   ├── autostart.go
│   ├── embed.go
│   ├── handler.go
│   ├── handler_ledger.go
│   ├── handler_ledger_test.go
│   ├── handler_memorymode_test.go
│   ├── handler_pipeline.go
│   ├── handler_test.go
│   ├── import.go
│   ├── import_realdata_test.go
│   ├── import_test.go
│   ├── network_handler.go
│   ├── pairing.go
│   ├── pairing_test.go
│   ├── redeploy_middleware.go
│   ├── sse.go
│   ├── sse_test.go
│   ├── update_handler.go
│   └── update_handler_test.go
├── buf.gen.yaml
├── CITATION.cff
├── CONTRIBUTING.md
├── Dockerfile
├── glama.json
├── go.mod
├── go.sum
├── LICENSE
├── Makefile
├── package.json
├── playwright.config.js
├── README.md
├── SECURITY.md
├── SECURITY_FAQ.md
└── server.json
```
