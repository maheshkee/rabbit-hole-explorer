import api_client
import sys

def test_api():
    topic = "Entropy"
    
    print("Running API tests...")
    
    # 1. Test POST /explore
    try:
        exploration = api_client.create_exploration(topic)
        exploration_id = exploration.get("exploration_id")
        
        if exploration_id is not None:
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
            
        # 3. Graph structure is valid
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
                print("✓ graph structure valid")
            else:
                print("✗ graph structure invalid: edges pointing to non-existent nodes")
                sys.exit(1)
        else:
            print("✗ graph structure invalid: nodes or edges are empty")
            sys.exit(1)
            
    except Exception as e:
        print(f"✗ graph retrieval failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_api()
