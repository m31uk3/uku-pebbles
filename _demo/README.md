# UKU Pebbles — MVP Demo

Functional demo of UKU Pebbles: book highlights as interconnected knowledge units.

## What it demonstrates

1. **Pebble creation** — Book highlights with full YAML attributes: location, timestamp, nearby people (opt-in consent), emotional state, book references, sharing permissions
2. **Natural language → sub-agent queries** — Vague queries like *"show me the important insights I made in the book at the coffee shop two weeks ago"* decompose into structured filters against YAML attributes
3. **Knowledge graph (red strings)** — Automatic connections between pebbles via matching YAML values, visualized with D3.js
4. **Drill-down** — From highlight → page → chapter → book, with links to all pebbles from that chapter
5. **Sharing & hive mind** — Aggregated views across people and groups (book club, individuals)

## Quick start

```bash
cd _demo
pip install -r requirements.txt
python -m sample_data.seed   # creates 10 sample pebbles
python app.py                # http://localhost:5000
```

## Sample data

10 pebbles from a reading-group scenario: a person reading *Meditations* by Marcus Aurelius across locations (coffee shops, library, park, transit, home) over two weeks, with friends who have opted in to proximity capture.

## Try these queries

- `show me the important insights I made in the book at the coffee shop two weeks ago`
- `highlights about stoicism when I was feeling inspired`
- `what did I read at the library last week`
- `notes with sarah about mindfulness #stoicism`
- `important reading notes from the park`

## Architecture

```
engine/
  pebble.py          — UKU data model (all YAML attributes from spec v2.1)
  store.py            — SQLite + JSON1 storage (mirrors Postgres JSONB spec)
  query_parser.py     — NL → sub-agent query decomposition
  knowledge_graph.py  — Red string computation + D3 graph builder
sample_data/
  seed.py             — 10 realistic book-reading pebbles
  vault/              — Generated .md files (Obsidian-compatible)
templates/            — Flask/Jinja2 UI
static/               — CSS
```
