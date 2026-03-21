# SAGE Interfaces

## REST API Endpoints

### Authentication
All authenticated endpoints require these headers:
```
X-Agent-ID: <ed25519_public_key_hex>
X-Signature: <ed25519_signature_hex>
X-Timestamp: <unix_seconds>
```

Signature is computed as: `Ed25519.Sign(SHA256(method + " " + path + "\n" + body) || BigEndian(timestamp))`

### Health & Status

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | No | Liveness check |
| GET | `/ready` | No | Readiness check (all services up) |
| GET | `/v1/dashboard/health` | No | Dashboard health with `vault_locked` flag |

#### GET /v1/dashboard/health — Response
```json
{
  "status": "ok",
  "vault_locked": false,
  "encrypted": true,
  "version": "5.0.7",
  "block_height": 42,
  "total_memories": 156
}
```

### Memory Operations

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/v1/memory/submit` | Yes | Propose new memory (on-chain tx) |
| GET | `/v1/memory/{id}` | Yes | Get memory by ID |
| GET | `/v1/memory/query` | Yes | Semantic similarity search |
| GET | `/v1/memory/list` | Yes | Browse memories with filters |
| POST | `/v1/memory/{id}/deprecate` | Yes | Deprecate memory (on-chain tx) |
| GET | `/v1/memory/timeline` | Yes | Time-bucketed memory view |
| POST | `/v1/memory/pre-validate` | Yes | Dry-run 4 validators (no on-chain) |

#### POST /v1/memory/submit — Request
```json
{
  "content": "The database migration requires a blue-green deployment strategy",
  "memory_type": "fact",
  "domain_tag": "infrastructure",
  "confidence_score": 0.85,
  "tags": ["migration", "deployment"],
  "agent_pub_key": "<hex>",
  "agent_sig": "<hex>",
  "body_hash": "<hex>",
  "timestamp": 1710000000
}
```

#### POST /v1/memory/submit — Response
```json
{
  "memory_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "proposed",
  "tx_hash": "<hex>"
}
```

#### GET /v1/memory/query — Parameters
| Param | Type | Description |
|-------|------|-------------|
| `q` | string | Search query text |
| `domain` | string | Filter by domain tag |
| `top_k` | int | Max results (default 10) |
| `min_confidence` | float | Minimum confidence threshold |
| `status` | string | Filter by status |

#### GET /v1/memory/list — Parameters
| Param | Type | Description |
|-------|------|-------------|
| `domain` | string | Filter by domain |
| `tag` | string | Filter by tag |
| `status` | string | Filter by status |
| `sort` | string | Sort field (created_at, confidence) |
| `order` | string | asc or desc |
| `limit` | int | Page size |
| `offset` | int | Page offset |

#### POST /v1/memory/pre-validate — Request
```json
{
  "content": "Hello world",
  "memory_type": "observation",
  "domain_tag": "general",
  "confidence_score": 0.5
}
```

#### POST /v1/memory/pre-validate — Response
```json
{
  "quorum_reached": false,
  "votes": [
    {"validator": "sentinel", "decision": "accept", "reason": "baseline accept"},
    {"validator": "dedup", "decision": "accept", "reason": "no duplicate found"},
    {"validator": "quality", "decision": "reject", "reason": "content too short (11 chars < 20 min)"},
    {"validator": "consistency", "decision": "accept", "reason": "all fields valid"}
  ],
  "accept_count": 3,
  "reject_count": 1
}
```

### Voting & Governance

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/v1/vote/submit` | Yes | Vote on proposed memory |
| GET | `/v1/vote/memory/{id}` | Yes | Get votes for a memory |

#### POST /v1/vote/submit — Request
```json
{
  "memory_id": "550e8400-...",
  "decision": "accept",
  "rationale": "Consistent with observed infrastructure patterns"
}
```

### Agent Management

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/v1/agent/register` | Yes | Register agent on-chain |
| GET | `/v1/agent/me` | Yes | Current agent profile |
| GET | `/v1/agent/{id}` | Yes | Get agent info |
| GET | `/v1/agents` | Yes | List all agents |
| PUT | `/v1/agent/{id}` | Yes | Update agent (on-chain) |

#### POST /v1/agent/register — Request
```json
{
  "name": "research-agent",
  "role": "researcher",
  "boot_bio": "I analyze scientific papers and extract key findings"
}
```

#### GET /v1/agent/me — Response
```json
{
  "agent_id": "a1b2c3d4...",
  "name": "research-agent",
  "role": "researcher",
  "clearance_level": 1,
  "provider": "claude-code",
  "poe_weight": 0.342,
  "vote_count": 28,
  "memory_count": 156,
  "registered_at": "2024-01-15T10:30:00Z"
}
```

### RBAC & Access Control

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/v1/access/grants` | Yes | List granted permissions |
| POST | `/v1/access/request` | Yes | Request domain access (on-chain) |
| POST | `/v1/access/grant` | Yes | Grant access (admin, on-chain) |
| POST | `/v1/access/revoke` | Yes | Revoke access (on-chain) |

#### POST /v1/access/grant — Request
```json
{
  "grantee_agent_id": "a1b2c3...",
  "domain_tag": "infrastructure",
  "access_level": "read",
  "clearance_level": 2,
  "expires_at": "2025-12-31T23:59:59Z"
}
```

### Organization & Federation

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/v1/org/register` | Yes | Register organization |
| GET | `/v1/orgs` | Yes | List organizations |
| POST | `/v1/org/{id}/member` | Yes | Add member |
| DELETE | `/v1/org/{id}/member/{agent_id}` | Yes | Remove member |

### Pipeline (Agent-to-Agent)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/v1/pipe/send` | Yes | Send message to another agent |
| GET | `/v1/pipe/check` | Yes | Check message delivery status |

#### POST /v1/pipe/send — Request
```json
{
  "target_agent_id": "b2c3d4...",
  "content": "Analysis complete. Found 3 anomalies.",
  "domain": "research"
}
```

### Configuration

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/v1/mcp-config` | No | Agent self-configure MCP connection |
| POST | `/v1/config/preferences` | Yes | Dashboard settings (memory mode, recall params) |

### Dashboard-Specific

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/v1/dashboard/login` | No | Vault unlock (passphrase required) |
| GET | `/v1/dashboard/status` | Session | Memory stats, domain counts, last activity |
| GET | `/v1/dashboard/events` | Session | SSE stream (real-time events) |
| GET | `/v1/ledger` | Session | Chain activity log |
| POST | `/v1/dashboard/cleanup` | Session | Deprecate cleanup candidates |

#### SSE Event Types (`/v1/dashboard/events`)
```
event: memory.stored      — New memory committed
event: memory.recalled    — Query result returned
event: memory.deprecated  — Memory deprecated
event: memory.challenge   — Dispute filed
event: memory.vote        — Validator voted
event: chain.block        — New block produced
```

---

## MCP Tools

All MCP tools are exposed via stdio JSON-RPC 2.0 when running `sage-gui mcp`.

### Memory Tools

#### sage_remember
Store a new memory in SAGE.
```json
{
  "content": "string (required)",
  "domain": "string (required)",
  "memory_type": "fact|observation|inference|task (default: observation)",
  "confidence": "float 0-1 (default: 0.7)",
  "tags": "string[] (optional)"
}
```

#### sage_recall
Search memories by semantic similarity.
```json
{
  "query": "string (required)",
  "domain": "string (optional — filter by domain)",
  "top_k": "int (default: 5)",
  "min_confidence": "float (optional)"
}
```

#### sage_forget
Deprecate a memory.
```json
{
  "memory_id": "string (required)",
  "reason": "string (optional)"
}
```

#### sage_list
Browse memories with filters.
```json
{
  "domain": "string (optional)",
  "tag": "string (optional)",
  "status": "string (optional)",
  "sort": "string (optional)",
  "limit": "int (optional)",
  "offset": "int (optional)"
}
```

#### sage_timeline
Time-grouped memory view.
```json
{
  "from": "ISO 8601 (optional)",
  "to": "ISO 8601 (optional)",
  "domain": "string (optional)"
}
```

#### sage_status
Get memory statistics (total count, domain breakdown, last activity).

### Agent Tools

#### sage_register
Register agent on-chain.
```json
{
  "name": "string (required)",
  "role": "string (optional)",
  "boot_bio": "string (optional)"
}
```

#### sage_agent_info
Get agent profile (PoE weight, vote count, memory count).

### Governance Tools

#### sage_vote
Vote on a proposed memory.
```json
{
  "memory_id": "string (required)",
  "decision": "accept|reject (required)",
  "rationale": "string (optional)"
}
```

#### sage_challenge
Dispute a memory.
```json
{
  "memory_id": "string (required)",
  "reason": "string (required)",
  "evidence": "string (optional)"
}
```

#### sage_corroborate
Provide supporting evidence for a memory.
```json
{
  "memory_id": "string (required)",
  "evidence": "string (required)"
}
```

### RBAC Tools

#### sage_access_request
Request access to a domain.
```json
{
  "domain": "string (required)",
  "access_level": "read|write (required)"
}
```

#### sage_access_list
List current access grants for the agent.

### Pipeline Tools

#### sage_pipe_send
Send message to another agent.
```json
{
  "target_agent_id": "string (required)",
  "content": "string (required)",
  "domain": "string (optional)"
}
```

#### sage_pipe_status
Check delivery status of a sent message.

---

## Internal Go Interfaces

### MemoryStore (`internal/store/store.go`)
```go
type MemoryStore interface {
    InsertMemory(ctx context.Context, record *memory.MemoryRecord) error
    GetMemory(ctx context.Context, id string) (*memory.MemoryRecord, error)
    UpdateStatus(ctx context.Context, id string, status string, at time.Time) error
    QuerySimilar(ctx context.Context, embedding []float32, opts QueryOptions) ([]*memory.MemoryRecord, error)
    ListMemories(ctx context.Context, opts ListOptions) ([]*memory.MemoryRecord, int, error)
    FindByContentHash(ctx context.Context, hash []byte) (bool, error)
    AddTag(ctx context.Context, memoryID, tag string) error
    RemoveTag(ctx context.Context, memoryID, tag string) error
    GetTags(ctx context.Context, memoryID string) ([]string, error)
    InsertVote(ctx context.Context, vote *ValidationVote) error
    GetVotesForMemory(ctx context.Context, memoryID string) ([]*ValidationVote, error)
    InsertChallenge(ctx context.Context, challenge *ChallengeEntry) error
    InsertCorroboration(ctx context.Context, corrob *Corroboration) error
}
```

### AccessStore (`internal/store/store.go`)
```go
type AccessStore interface {
    GrantAccess(ctx context.Context, grant *AccessGrant) error
    RevokeAccess(ctx context.Context, granteeID, domain string) error
    GetGrants(ctx context.Context, agentID string) ([]*AccessGrant, error)
    CheckAccess(ctx context.Context, agentID, domain, level string) (bool, error)
    InsertAccessLog(ctx context.Context, log *AccessLog) error
}
```

### OrgStore (`internal/store/store.go`)
```go
type OrgStore interface {
    RegisterOrg(ctx context.Context, org *OrgInfo) error
    GetOrg(ctx context.Context, orgID string) (*OrgInfo, error)
    ListOrgs(ctx context.Context) ([]*OrgInfo, error)
    AddMember(ctx context.Context, orgID, agentID string, clearance int) error
    RemoveMember(ctx context.Context, orgID, agentID string) error
    GetMembers(ctx context.Context, orgID string) ([]*OrgMember, error)
}
```

### AgentStore (`internal/store/store.go`)
```go
type AgentStore interface {
    RegisterAgent(ctx context.Context, agent *AgentInfo) error
    GetAgent(ctx context.Context, agentID string) (*AgentInfo, error)
    UpdateAgent(ctx context.Context, agent *AgentInfo) error
    ListAgents(ctx context.Context) ([]*AgentInfo, error)
}
```

### ValidatorScoreStore (`internal/store/store.go`)
```go
type ValidatorScoreStore interface {
    GetScore(ctx context.Context, validatorID string) (*ValidatorScore, error)
    UpdateScore(ctx context.Context, score *ValidatorScore) error
    GetAllScores(ctx context.Context) ([]*ValidatorScore, error)
    InsertEpochScore(ctx context.Context, epoch *EpochScore) error
}
```

### Validator (`internal/appvalidator/validator.go`)
```go
type Validator interface {
    Name() string
    Validate(content string, contentHash []byte, domain string, memType string, confidence float64) VoteResult
}
```

### Embedding Provider (`internal/embedding/provider.go`)
```go
type Provider interface {
    Embed(ctx context.Context, text string) ([]float32, error)
}
```

### RedeployOrchestrator (`internal/orchestrator/redeployer.go`)
```go
type RedeployOrchestrator interface {
    DeployOp(ctx context.Context, op string, agentID string) error
    GetRedeployStatus(ctx context.Context) (active bool, operation string, agentID string, err error)
}
```

---

## Protobuf Definitions (`api/proto/sage/v1/`)

### Transaction Types (`tx.proto`)
```protobuf
message SageTx {
    oneof payload {
        MemorySubmitTx submit = 1;
        MemoryVoteTx vote = 2;
        MemoryChallengeTx challenge = 3;
        MemoryCorrobTx corrob = 4;
    }
    bytes signature = 10;
    bytes public_key = 11;
    uint64 nonce = 12;
    google.protobuf.Timestamp timestamp = 13;
}

message MemorySubmitTx {
    string memory_id = 1;
    bytes content_hash = 2;
    bytes embedding_hash = 3;
    MemoryType memory_type = 4;
    string domain_tag = 5;
    double confidence_score = 6;
    string content = 7;
    string parent_hash = 8;
}

message MemoryVoteTx {
    string memory_id = 1;
    VoteDecision decision = 2;
    string rationale = 3;
}
```

### Query Types (`query.proto`)
```protobuf
message QueryMemoryRequest {
    string memory_id = 1;
}

message QuerySimilarRequest {
    repeated float embedding = 1;
    string domain_tag = 2;
    int32 top_k = 3;
    double min_confidence = 4;
}
```

---

## Python SDK API (`sdk/python/`)

### SageClient
```python
from sage_sdk import SageClient, AgentIdentity

identity = AgentIdentity.generate()  # or .from_file(), .from_seed()
client = SageClient(base_url="http://localhost:8080", identity=identity)

# Memory
result = client.propose(content, memory_type, domain_tag, confidence)
matches = client.query(embedding, domain_tag, min_confidence, top_k)
client.forget(memory_id)
memories = client.list(domain, tag, status)

# Voting
client.vote(memory_id, decision, rationale)
client.challenge(memory_id, reason, evidence)
client.corroborate(memory_id, evidence)

# Agent
reg = client.register_agent(name, role, boot_bio)
profile = client.get_profile()
agent = client.get_agent(agent_id)

# RBAC
client.set_agent_permission(agent_id, clearance, org_id)

# Organizations
client.register_org(name)
client.add_org_member(org_id, agent_id, clearance)

# Health
health = client.health()
ready = client.ready()
```

### AsyncClient
Same API as SageClient but with `async`/`await` using httpx.
