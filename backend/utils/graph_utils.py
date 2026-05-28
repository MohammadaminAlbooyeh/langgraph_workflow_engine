from __future__ import annotations
from typing import Any
from backend.utils.exceptions import InvalidGraphError


def topological_sort(nodes: list[dict], edges: list[dict]) -> list[str]:
    adj = {n["id"]: [] for n in nodes}
    in_degree = {n["id"]: 0 for n in nodes}

    for edge in edges:
        src, tgt = edge["source_id"], edge["target_id"]
        adj[src].append(tgt)
        in_degree[tgt] = in_degree.get(tgt, 0) + 1

    queue = [nid for nid, deg in in_degree.items() if deg == 0]
    result = []

    while queue:
        node = queue.pop(0)
        result.append(node)
        for neighbor in adj.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(nodes):
        raise InvalidGraphError("Graph contains a cycle")
    return result


def find_cycles(edges: list[dict]) -> list[list[str]]:
    adj = {}
    for edge in edges:
        src, tgt = edge["source_id"], edge["target_id"]
        adj.setdefault(src, []).append(tgt)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {}
    cycles = []

    def dfs(node, path):
        color[node] = GRAY
        path.append(node)
        for neighbor in adj.get(node, []):
            if color.get(neighbor) == GRAY:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
            elif color.get(neighbor) == WHITE:
                dfs(neighbor, path)
        path.pop()
        color[node] = BLACK

    all_nodes = set()
    for e in edges:
        all_nodes.add(e["source_id"])
        all_nodes.add(e["target_id"])
    for n in all_nodes:
        color.setdefault(n, WHITE)

    for n in all_nodes:
        if color[n] == WHITE:
            dfs(n, [])
    return cycles


def get_node_by_id(nodes: list[dict], node_id: str) -> dict | None:
    for node in nodes:
        if node["id"] == node_id:
            return node
    return None


def validate_graph(nodes: list[dict], edges: list[dict]) -> list[str]:
    errors = []
    if not nodes:
        errors.append("Graph must have at least one node")
        return errors

    node_ids = {n["id"] for n in nodes}
    for i, node in enumerate(nodes):
        if not node.get("id"):
            errors.append(f"Node at index {i} is missing an id")

    for edge in edges:
        if edge["source_id"] not in node_ids:
            errors.append(f"Edge source '{edge['source_id']}' not found in nodes")
        if edge["target_id"] not in node_ids:
            errors.append(f"Edge target '{edge['target_id']}' not found in nodes")

    try:
        topsort = topological_sort(nodes, edges)
    except InvalidGraphError:
        cycles = find_cycles(edges)
        for cycle in cycles:
            errors.append(f"Cycle detected: {' -> '.join(cycle)}")

    return errors
