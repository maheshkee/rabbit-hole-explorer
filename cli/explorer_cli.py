import argparse
import sys
import json
import api_client
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Rabbit Hole Explorer CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Explore command
    explore_parser = subparsers.add_parser("explore", help="Start a new exploration")
    explore_parser.add_argument("topic", type=str, help="The topic to explore")

    # Graph command
    graph_parser = subparsers.add_parser("graph", help="Retrieve an exploration graph")
    graph_parser.add_argument("exploration_id", type=int, help="The ID of the exploration")

    # Expand command
    expand_parser = subparsers.add_parser("expand", help="Expand an existing node")
    expand_parser.add_argument("node_id", type=int, help="The ID of the node to expand")

    # Health command
    subparsers.add_parser("health", help="Check backend health")

    # Test command
    subparsers.add_parser("test", help="Run API tests")

    args = parser.parse_args()

    try:
        if args.command == "explore":
            result = api_client.create_exploration(args.topic)
            print(json.dumps(result, indent=2))
        elif args.command == "graph":
            result = api_client.get_exploration_graph(args.exploration_id)
            print(json.dumps(result, indent=2))
        elif args.command == "expand":
            result = api_client.expand_node(args.node_id)
            print(json.dumps(result, indent=2))
        elif args.command == "health":
            result = api_client.get_health()
            print(json.dumps(result, indent=2))
        elif args.command == "test":
            print("Running API tests...")
            import os
            test_path = os.path.join(os.path.dirname(__file__), "test_api.py")
            result = subprocess.run([sys.executable, test_path], check=False)
            if result.returncode != 0:
                sys.exit(result.returncode)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
