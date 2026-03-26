"""
UKU Pebbles MVP — Interactive Demo

Demonstrates:
  1. Book highlights as pebbles with full YAML attributes
  2. Natural language → sub-agent query decomposition
  3. Knowledge graph visualization (red strings)
  4. Drill-down with semantic inference via book references
  5. Sharing and aggregation between people/groups
"""

import json
import os
import sys

from flask import Flask, render_template, request, jsonify

sys.path.insert(0, os.path.dirname(__file__))

from engine.store import init_db, get_all_pebbles, get_pebble, search_pebbles, find_red_strings, DB_PATH
from engine.query_parser import parse_query, merge_filters, format_query_plan
from engine.knowledge_graph import build_graph, build_ego_graph

app = Flask(__name__)


@app.before_request
def ensure_db():
    if not os.path.exists(DB_PATH):
        from sample_data.seed import seed
        seed()


@app.route("/")
def index():
    pebbles = get_all_pebbles()
    return render_template("index.html", pebbles=pebbles)


@app.route("/query", methods=["POST"])
def query():
    """
    Natural language query → sub-agent decomposition → results.

    This is the core demo: take a vague human query and show exactly
    how it maps to structured YAML attribute filters.
    """
    text = request.json.get("query", "")
    if not text:
        return jsonify({"error": "No query provided"}), 400

    # Step 1: Parse natural language into sub-agent queries
    parsed = parse_query(text)

    # Step 2: Merge filters and search
    filters = merge_filters(parsed.sub_queries)
    results = search_pebbles(filters)

    # Step 3: Build knowledge graph of results
    graph = build_graph(results)

    return jsonify({
        "original_query": parsed.original,
        "explanation": parsed.explanation,
        "query_plan": format_query_plan(parsed),
        "results": [
            {
                "uku_id": r["yaml_data"]["uku_id"],
                "title": r["yaml_data"].get("title", ""),
                "body": r.get("body_text", ""),
                "yaml": r["yaml_data"],
            }
            for r in results
        ],
        "graph": graph,
        "result_count": len(results),
    })


@app.route("/pebble/<uku_id>")
def pebble_detail(uku_id):
    """Single pebble view with drill-down and red string connections."""
    pebble = get_pebble(uku_id)
    if not pebble:
        return "Pebble not found", 404

    red_strings = find_red_strings(uku_id)
    all_pebbles = get_all_pebbles()
    ego_graph = build_ego_graph(uku_id, all_pebbles)

    return render_template(
        "pebble.html",
        pebble=pebble,
        red_strings=red_strings,
        ego_graph=json.dumps(ego_graph),
    )


@app.route("/graph")
def graph_view():
    """Full knowledge graph of all pebbles."""
    pebbles = get_all_pebbles()
    graph = build_graph(pebbles)
    return render_template("graph.html", graph=json.dumps(graph))


@app.route("/shared/<person_or_group>")
def shared_view(person_or_group):
    """View pebbles shared with a person or group — hive mind aggregation."""
    all_pebbles = get_all_pebbles()
    matching = []
    for p in all_pebbles:
        yaml = p["yaml_data"]
        shared_with = yaml.get("shared_with", [])
        shared_groups = yaml.get("shared_with_groups", [])
        people = yaml.get("people", [])
        creator = yaml.get("creator", "")

        if (person_or_group in shared_with or
            person_or_group in shared_groups or
            person_or_group in people or
            person_or_group == creator):
            matching.append(p)

    graph = build_graph(matching)
    return render_template(
        "shared.html",
        entity=person_or_group,
        pebbles=matching,
        graph=json.dumps(graph),
    )


@app.route("/api/pebbles")
def api_pebbles():
    return jsonify(get_all_pebbles())


@app.route("/api/graph")
def api_graph():
    pebbles = get_all_pebbles()
    return jsonify(build_graph(pebbles))


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        from sample_data.seed import seed
        seed()
    app.run(debug=True, port=5000)
