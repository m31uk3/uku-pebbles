"""
Knowledge graph builder — computes red strings between pebbles
and produces graph data for visualization.
"""

from .store import get_all_pebbles, find_red_strings, _find_matching_attrs


def build_graph(pebbles: list[dict]) -> dict:
    """
    Build a knowledge graph from a list of pebbles.

    Returns {nodes: [...], edges: [...]} suitable for D3.js force graph.
    """
    nodes = []
    edges = []
    seen_edges = set()

    for p in pebbles:
        yaml = p["yaml_data"]
        node = {
            "id": yaml.get("uku_id", ""),
            "title": yaml.get("title", "Untitled"),
            "uku_type": yaml.get("uku_type", ""),
            "category": yaml.get("category", ""),
            "weight": yaml.get("weight", 0.5),
            "tags": yaml.get("tags", []),
            "location": yaml.get("location", {}).get("name", "") if isinstance(yaml.get("location"), dict) else "",
            "created_at": yaml.get("created_at", ""),
            "book": yaml.get("book_ref", {}).get("book_title", "") if isinstance(yaml.get("book_ref"), dict) else "",
            "people": yaml.get("people", []),
        }
        nodes.append(node)

    # Compute red strings between all pairs
    for i, p1 in enumerate(pebbles):
        for j, p2 in enumerate(pebbles):
            if j <= i:
                continue

            connections = _find_matching_attrs(p1["yaml_data"], p2["yaml_data"])
            if connections:
                edge_key = tuple(sorted([p1["yaml_data"]["uku_id"], p2["yaml_data"]["uku_id"]]))
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    edges.append({
                        "source": p1["yaml_data"]["uku_id"],
                        "target": p2["yaml_data"]["uku_id"],
                        "connections": connections,
                        "strength": len(connections),
                        "labels": [c["path"] for c in connections],
                    })

    return {"nodes": nodes, "edges": edges}


def build_ego_graph(center_id: str, pebbles: list[dict], max_depth: int = 2) -> dict:
    """
    Build an ego-centric graph centered on one pebble.
    Shows direct connections (depth 1) and connections-of-connections (depth 2).
    """
    center = None
    for p in pebbles:
        if p["yaml_data"].get("uku_id") == center_id:
            center = p
            break

    if not center:
        return {"nodes": [], "edges": []}

    included_ids = {center_id}
    all_edges = []

    # Depth 1: direct connections
    for p in pebbles:
        if p["yaml_data"].get("uku_id") == center_id:
            continue
        connections = _find_matching_attrs(center["yaml_data"], p["yaml_data"])
        if connections:
            included_ids.add(p["yaml_data"]["uku_id"])
            all_edges.append({
                "source": center_id,
                "target": p["yaml_data"]["uku_id"],
                "connections": connections,
                "strength": len(connections),
                "labels": [c["path"] for c in connections],
                "depth": 1,
            })

    # Depth 2: connections of connections
    if max_depth >= 2:
        depth1_ids = set(included_ids) - {center_id}
        for d1_id in depth1_ids:
            d1_pebble = None
            for p in pebbles:
                if p["yaml_data"].get("uku_id") == d1_id:
                    d1_pebble = p
                    break
            if not d1_pebble:
                continue

            for p in pebbles:
                pid = p["yaml_data"].get("uku_id")
                if pid in included_ids:
                    continue
                connections = _find_matching_attrs(d1_pebble["yaml_data"], p["yaml_data"])
                if connections and len(connections) >= 2:  # Require stronger connection at depth 2
                    included_ids.add(pid)
                    all_edges.append({
                        "source": d1_id,
                        "target": pid,
                        "connections": connections,
                        "strength": len(connections),
                        "labels": [c["path"] for c in connections],
                        "depth": 2,
                    })

    nodes = []
    for p in pebbles:
        pid = p["yaml_data"].get("uku_id")
        if pid in included_ids:
            yaml = p["yaml_data"]
            nodes.append({
                "id": pid,
                "title": yaml.get("title", "Untitled"),
                "uku_type": yaml.get("uku_type", ""),
                "category": yaml.get("category", ""),
                "weight": yaml.get("weight", 0.5),
                "tags": yaml.get("tags", []),
                "location": yaml.get("location", {}).get("name", "") if isinstance(yaml.get("location"), dict) else "",
                "created_at": yaml.get("created_at", ""),
                "book": yaml.get("book_ref", {}).get("book_title", "") if isinstance(yaml.get("book_ref"), dict) else "",
                "people": yaml.get("people", []),
                "is_center": pid == center_id,
            })

    return {"nodes": nodes, "edges": all_edges}
