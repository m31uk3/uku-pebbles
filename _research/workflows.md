# SAGE Workflows

## 1. Memory Submission Pipeline

```mermaid
sequenceDiagram
    participant Agent as AI Agent
    participant MCP as MCP Server
    participant REST as REST API
    participant AppVal as App Validators
    participant ABCI as ABCI App
    participant Comet as CometBFT
    participant Store as Storage

    Agent->>MCP: sage_remember(content, domain, type)
    MCP->>REST: POST /v1/memory/pre-validate
    REST->>AppVal: Run 4 validators
    AppVal-->>REST: VoteResults (3/4 accept?)

    alt Quorum NOT reached
        REST-->>MCP: Rejected (reason)
        MCP-->>Agent: Memory rejected
    else Quorum reached
        REST-->>MCP: Pre-validation passed
        MCP->>REST: POST /v1/memory/submit
        REST->>REST: Generate UUID, compute SHA-256 hash
        REST->>REST: Generate embedding (Ollama)
        REST->>REST: Sign transaction (Ed25519)
        REST->>Comet: BroadcastTxSync(protobuf)
        Comet->>ABCI: CheckTx (verify sig, nonce)
        ABCI-->>Comet: OK
        Comet->>Comet: Include in next block
        Comet->>ABCI: FinalizeBlock
        ABCI->>ABCI: processMemorySubmit()
        ABCI->>ABCI: Verify agent proof
        ABCI->>ABCI: Check domain access
        ABCI->>ABCI: Buffer write
        Comet->>ABCI: Commit
        ABCI->>Store: Atomic flush (memory + status)
        Store-->>ABCI: OK
        ABCI-->>Comet: AppHash
        REST-->>MCP: {memory_id, status: "proposed"}
        MCP-->>Agent: Memory stored
    end
```

### Steps
1. Agent calls `sage_remember` via MCP
2. MCP server calls `/v1/memory/pre-validate` to dry-run 4 validators
3. If 3/4 validators accept, MCP proceeds to `/v1/memory/submit`
4. REST handler: generates UUID, computes SHA-256 content hash, generates embedding
5. REST handler: encodes protobuf transaction, signs with node key
6. Transaction broadcast to CometBFT via `BroadcastTxSync`
7. CometBFT calls `CheckTx` — ABCI verifies signature and nonce
8. Transaction included in next block (~3s block time)
9. CometBFT calls `FinalizeBlock` — ABCI processes memory submit
10. On-chain: verify agent proof, check domain access, buffer write
11. CometBFT calls `Commit` — ABCI flushes all buffered writes atomically
12. Memory stored with status "proposed"

## 2. Consensus Voting

```mermaid
sequenceDiagram
    participant V1 as Validator 1
    participant V2 as Validator 2
    participant V3 as Validator 3
    participant V4 as Validator 4
    participant ABCI as ABCI App
    participant PoE as PoE Engine
    participant Store as Storage

    Note over V1,V4: Memory proposed (status: proposed)

    V1->>ABCI: VoteTx(memory_id, accept)
    ABCI->>PoE: Get weight for V1 in domain
    PoE-->>ABCI: weight = 0.35
    ABCI->>ABCI: Record vote, check quorum
    Note over ABCI: 1/4 voted, quorum not met

    V2->>ABCI: VoteTx(memory_id, accept)
    ABCI->>PoE: Get weight for V2
    PoE-->>ABCI: weight = 0.28
    ABCI->>ABCI: Record vote, check quorum
    Note over ABCI: 2/4 voted, quorum not met

    V3->>ABCI: VoteTx(memory_id, reject)
    ABCI->>PoE: Get weight for V3
    PoE-->>ABCI: weight = 0.22
    ABCI->>ABCI: Record vote, check quorum
    Note over ABCI: 3/4 voted

    V4->>ABCI: VoteTx(memory_id, accept)
    ABCI->>PoE: Get weight for V4
    PoE-->>ABCI: weight = 0.15
    ABCI->>ABCI: Record vote, check quorum
    Note over ABCI: 4/4 voted

    ABCI->>ABCI: checkAndApplyQuorum()
    Note over ABCI: accept_weight=0.78, total=1.0<br/>0.78 >= 2/3 threshold
    ABCI->>Store: UpdateStatus(committed)
    ABCI->>PoE: RecordVote outcomes
```

### Steps
1. After a memory is proposed, validators submit vote transactions
2. Each vote is weighted by the PoE engine based on validator expertise
3. Weight formula: `exp(0.4·ln(accuracy) + 0.3·ln(domain) + 0.15·ln(recency) + 0.15·ln(corroboration))`
4. 10% reputation cap prevents single-validator dominance
5. `checkAndApplyQuorum()` runs after each vote
6. Quorum requires weighted accept votes ≥ 2/3 of total weight
7. If quorum reached: status → "committed"
8. If quorum impossible (too many rejects): status → "deprecated"
9. PoE engine records vote outcomes for future weight calculations

## 3. RBAC Access Control Flow

```mermaid
sequenceDiagram
    participant Agent as Querying Agent
    participant REST as REST API
    participant Badger as BadgerDB
    participant Store as MemoryStore

    Agent->>REST: GET /v1/memory/list?domain=research
    REST->>REST: Extract X-Agent-ID from headers

    REST->>Badger: Check Gate 1: Direct agent match
    alt Agent owns the memory
        Badger-->>REST: Visible
    else Not owner
        REST->>Badger: Check Gate 2: Domain access grant
        alt Agent has domain grant with sufficient clearance
            Badger-->>REST: Visible
        else No domain grant
            REST->>Badger: Check Gate 3: Org membership
            alt Same org as memory author
                Badger-->>REST: Visible
            else Different org
                REST->>Badger: Check Gate 4: Federation
                alt Orgs are federated
                    Badger-->>REST: Visible
                else No federation
                    Badger-->>REST: NOT visible
                end
            end
        end
    end

    REST->>Store: Query with visibility filter
    Store-->>REST: Filtered results
    REST-->>Agent: Only authorized memories
```

### Access Control Gates (checked in order)
1. **Direct agent match** — Agent submitted the memory → always visible
2. **Domain access grant** — Agent has explicit read/write on the domain AND agent clearance ≥ memory clearance level
3. **Organization membership** — Agent is in the same org as the memory author
4. **Federation** — Agent's org and author's org have approved federation
5. **Default** — Fail-secure: not visible

DomainAccess and multi-org gates are **alternatives**, not stacked. Passing one skips the others.

## 4. Vault Encryption Lifecycle

```mermaid
sequenceDiagram
    participant User as User
    participant Dash as CEREBRUM Dashboard
    participant Web as Web Handler
    participant Vault as Vault
    participant Store as Storage

    Note over User,Store: Initial Setup
    User->>Dash: Set vault passphrase
    Dash->>Web: POST /v1/dashboard/login
    Web->>Vault: Argon2id(passphrase → 256-bit key)
    Vault-->>Web: AES-256-GCM key ready
    Web->>Web: Generate recovery key
    Web-->>Dash: Recovery key (save this!)

    Note over User,Store: Normal Operation (Unlocked)
    User->>Dash: Submit memory
    Dash->>Web: POST /v1/memory/submit
    Web->>Vault: Encrypt(content)
    Vault-->>Web: "enc::BASE64(nonce||ciphertext||tag)"
    Web->>Store: Store encrypted content

    Note over User,Store: Read Operation (Unlocked)
    User->>Dash: View memory
    Dash->>Web: GET /v1/memory/{id}
    Web->>Store: Get encrypted content
    Store-->>Web: "enc::BASE64(...)"
    Web->>Vault: Decrypt(ciphertext)
    Vault-->>Web: Plaintext content
    Web-->>Dash: Display content

    Note over User,Store: Locked State
    User->>Dash: View memory (vault locked)
    Dash->>Web: GET /v1/memory/{id}
    Web-->>Dash: "[encrypted — vault locked]"

    Note over User,Store: Write Rejected (Locked)
    User->>Dash: Submit memory (vault locked)
    Dash->>Web: POST /v1/memory/submit
    Web-->>Dash: Error: vault locked, unlock via CEREBRUM
```

### Key Points
- Passphrase → Argon2id → 256-bit AES key (memory-hard, GPU-resistant)
- Encrypted format: `enc::<base64(12-byte nonce || ciphertext || GCM tag)>`
- When locked: reads return placeholder, writes are rejected
- Recovery key allows passphrase reset without data loss
- Vault key file auto-backed up on upgrade

## 5. Agent Registration

```mermaid
sequenceDiagram
    participant Agent as AI Agent
    participant MCP as MCP Server
    participant REST as REST API
    participant ABCI as ABCI App
    participant Badger as BadgerDB

    Agent->>MCP: sage_register(name, role, bio)
    MCP->>MCP: Generate Ed25519 keypair (if first time)
    MCP->>MCP: Save key to SAGE_HOME/agent.key
    MCP->>REST: POST /v1/agent/register
    REST->>REST: Sign with agent key
    REST->>ABCI: AgentRegisterTx (on-chain)
    ABCI->>ABCI: Verify signature
    ABCI->>Badger: Store agent identity
    Badger-->>ABCI: OK
    ABCI-->>REST: Agent registered
    REST-->>MCP: {agent_id, name, role}
    MCP-->>Agent: Registration confirmed

    Note over Agent,Badger: Auto-registration on first MCP connection
```

### Steps
1. On first MCP connection, `sage-gui` generates Ed25519 keypair
2. Key saved to `SAGE_HOME/agent.key`
3. Agent ID = hex-encoded public key
4. Registration transaction submitted on-chain
5. BadgerDB stores agent identity (name, role, clearance, provider)
6. Subsequent connections auto-authenticate with saved key

## 6. LAN Pairing

```mermaid
sequenceDiagram
    participant Admin as Admin Dashboard
    participant Web as Web Handler
    participant Pair as PairingStore
    participant NewAgent as New Agent

    Admin->>Web: POST /v1/pairing/code
    Web->>Pair: Generate 6-char code (5 min TTL)
    Pair-->>Web: Code: "A3X9K2"
    Web-->>Admin: Display pairing code

    NewAgent->>Web: GET /v1/pairing/fetch-config?code=A3X9K2
    Web->>Pair: Validate code
    alt Code valid and not expired
        Pair-->>Web: OK
        Web->>Web: Generate agent keypair
        Web->>Web: Create agent config bundle
        Web-->>NewAgent: {agent_key, mcp_config, server_url}
        Web->>Pair: Invalidate code (single-use)
    else Code invalid or expired
        Web-->>NewAgent: Error: invalid pairing code
    end
```

## 7. Network Redeployment (9-Phase State Machine)

```mermaid
sequenceDiagram
    participant Admin as Admin Agent
    participant Orch as Orchestrator
    participant Nodes as Network Nodes

    Admin->>Orch: DeployOp(reconfig, agentID)

    Note over Orch: Phase 1: Propose
    Orch->>Orch: Lock writes

    Note over Orch: Phase 2: Pause Consensus
    Orch->>Nodes: Pause block production

    Note over Orch: Phase 3: Backup State
    Orch->>Nodes: Snapshot BadgerDB + PostgreSQL

    Note over Orch: Phase 4: Reconfigure Validators
    Orch->>Nodes: Update validator set, keys

    Note over Orch: Phase 5: Restart Nodes
    Orch->>Nodes: Stop and restart with new config

    Note over Orch: Phase 6: Verify Quorum
    Orch->>Nodes: Check all nodes online

    alt Quorum not established
        Note over Orch: ROLLBACK
        Orch->>Nodes: Restore from backup
    else Quorum OK
        Note over Orch: Phase 7: Resume Consensus
        Orch->>Nodes: Resume block production

        Note over Orch: Phase 8: Migrate Data
        Orch->>Nodes: Re-replicate state to new validators

        Note over Orch: Phase 9: Cleanup
        Orch->>Orch: Remove backups, unlock writes
    end

    Orch-->>Admin: Deployment complete
```

### Key Features
- Rollback possible at every phase
- Writes locked during redeployment (REST returns 503 via middleware)
- State backed up before any changes
- CometBFT 1/3 max power change constraint enforced

## 8. MCP Tool Execution

```mermaid
sequenceDiagram
    participant AI as AI Agent
    participant MCP as MCP Server (stdio)
    participant REST as REST API
    participant Store as Storage

    AI->>MCP: JSON-RPC 2.0 request<br/>{method: "tools/call", params: {name: "sage_recall"}}
    MCP->>MCP: Parse tool name and arguments
    MCP->>MCP: Check memory mode (full/bookend/on-demand)

    alt Mode allows this operation
        MCP->>MCP: Sign request with agent key
        MCP->>REST: GET /v1/memory/query?q=...
        REST->>REST: Verify signature
        REST->>Store: QuerySimilar(embedding, opts)
        Store-->>REST: Matching memories
        REST-->>MCP: JSON response
        MCP->>MCP: Format results for agent
        MCP-->>AI: JSON-RPC 2.0 response
    else Mode blocks operation
        MCP-->>AI: Skipped (memory mode: on-demand)
    end

    MCP->>MCP: Increment callsSinceTurn

    alt Auto-turn enabled (full mode)
        Note over MCP: After N calls, auto-trigger sage_turn
    end
```

### Memory Mode Behavior
| Mode | Boot | Turn | Reflect | Manual |
|------|------|------|---------|--------|
| `full` | Load inception memories | Auto-save observations | Save reflections | Always available |
| `bookend` | Load inception memories | Skip | Save reflections | Always available |
| `on-demand` | Skip | Skip | Skip | Only explicit sage_remember |

## 9. Dashboard SSE Events

```mermaid
sequenceDiagram
    participant Browser as CEREBRUM Dashboard
    participant SSE as SSE Broadcaster
    participant Web as Web Handler
    participant ABCI as ABCI App

    Browser->>SSE: GET /v1/dashboard/events (EventSource)
    SSE-->>Browser: Connection established

    Note over ABCI: Memory committed in block
    ABCI->>Web: OnEvent(memory.stored, data)
    Web->>SSE: Broadcast to all clients
    SSE-->>Browser: event: memory.stored<br/>data: {memory_id, domain, type}

    Browser->>Browser: Update brain graph in real-time

    Note over ABCI: Vote recorded
    ABCI->>Web: OnEvent(memory.vote, data)
    Web->>SSE: Broadcast
    SSE-->>Browser: event: memory.vote<br/>data: {memory_id, validator, decision}

    Browser->>Browser: Update vote count display
```

### Event Types
- `memory.stored` — New memory committed to chain
- `memory.recalled` — Query executed, results returned
- `memory.deprecated` — Memory deprecated
- `memory.challenge` — Dispute filed against memory
- `memory.vote` — Validator voted on memory
- `chain.block` — New block produced

## 10. Pre-Validation Flow

```mermaid
sequenceDiagram
    participant Client as Client
    participant REST as REST API
    participant S as Sentinel
    participant D as Dedup
    participant Q as Quality
    participant C as Consistency

    Client->>REST: POST /v1/memory/pre-validate
    REST->>S: Validate(content, hash, domain, type, confidence)
    S-->>REST: {decision: "accept", reason: "baseline accept"}

    REST->>D: Validate(content, hash, domain, type, confidence)
    D->>D: Check SHA-256 hash against existing
    D-->>REST: {decision: "accept", reason: "no duplicate"}

    REST->>Q: Validate(content, hash, domain, type, confidence)
    Q->>Q: Check length >= 20, not greeting noise
    Q-->>REST: {decision: "reject", reason: "content too short"}

    REST->>C: Validate(content, hash, domain, type, confidence)
    C->>C: Check confidence 0-1, required fields
    C-->>REST: {decision: "accept", reason: "all fields valid"}

    REST->>REST: Count: 3 accept, 1 reject (3/4 = quorum)
    REST-->>Client: {quorum_reached: true, votes: [...]}
```

### Validator Behavior
| Validator | Accept When | Reject When |
|-----------|-------------|-------------|
| Sentinel | Always | Never (ensures liveness) |
| Dedup | No matching SHA-256 hash | Duplicate content exists |
| Quality | Length ≥ 20, not greeting noise | Too short, greeting phrases, empty headers |
| Consistency | Valid confidence (0-1), required fields present | Out-of-range confidence, missing fields |
