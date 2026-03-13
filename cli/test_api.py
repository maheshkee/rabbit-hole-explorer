import api_client
import sys

def test_api():
    topic = "Entropy"

    print("Running API tests...")

    # 1. Test POST /explore
    try:
        exploration = api_client.create_exploration(topic)
        exploration_id = exploration.get("exploration_id")

        if isinstance(exploration_id, int):
            print("✓ explore endpoint working")
        else:
            print("✗ explore endpoint failed: no exploration_id returned")
            sys.exit(1)

    except Exception as e:
        print(f"✗ explore endpoint failed: {e}")
        sys.exit(1)

    # 2. Test GET /explorations/{id}
    try:
        graph = api_client.get_exploration_graph(exploration_id)

        if "nodes" in graph and "edges" in graph:
            print("✓ graph retrieval working")
        else:
            print("✗ graph retrieval failed: nodes or edges missing from response")
            sys.exit(1)

        # 3. Graph integrity is valid
        nodes = graph["nodes"]
        edges = graph["edges"]

        if len(nodes) > 0 and len(edges) > 0:
            node_ids = {node["id"] for node in nodes}
            valid_edges = True
            for edge in edges:
                if edge["source"] not in node_ids or edge["target"] not in node_ids:
                    valid_edges = False
                    break

            if valid_edges:
                print("✓ graph integrity valid")
            else:
                print("✗ graph integrity invalid: edges point to non-existent nodes")
                sys.exit(1)
        else:
            print("✗ graph integrity invalid: nodes or edges are empty")
            sys.exit(1)

        # 4. Test POST /nodes/{node_id}/expand
        node_id_to_expand = nodes[0]["id"]
        expansion_result = api_client.expand_node(node_id_to_expand)
        new_node_titles = expansion_result.get("new_nodes", [])

        if expansion_result.get("node_id") == node_id_to_expand and len(new_node_titles) > 0:
            print("✓ node expansion working")
        else:
            print(f"✗ node expansion failed: {expansion_result}")
            sys.exit(1)

        # 5. Verify graph updated with new nodes and edges
        updated_graph = api_client.get_exploration_graph(exploration_id)
        updated_nodes = updated_graph["nodes"]
        updated_edges = updated_graph["edges"]

        if len(updated_nodes) > len(nodes) and len(updated_edges) > len(edges):
             updated_node_ids = {node["id"] for node in updated_nodes}
             updated_node_titles = {node["title"] for node in updated_nodes}
             invalid_edges = [
                 edge for edge in updated_edges
                 if edge["source"] not in updated_node_ids or edge["target"] not in updated_node_ids
             ]

             if invalid_edges:
                 print("✗ graph integrity invalid after expansion")
                 sys.exit(1)
             if not set(new_node_titles).issubset(updated_node_titles):
                 print("✗ graph update failed: expanded nodes missing from graph")
                 sys.exit(1)
        else:
             print(
                 f"✗ graph update failed: nodes {len(updated_nodes)} vs {len(nodes)}, "
                 f"edges {len(updated_edges)} vs {len(edges)}"
             )
             sys.exit(1)

    except Exception as e:
        print(f"✗ graph retrieval failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_api()
