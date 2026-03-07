# Rabbit Hole Explorer - Backend

This is the backend for the Rabbit Hole Explorer application.

## CLI Usage

The backend includes a CLI tool for interaction and verification.

### Setup

Ensure you have the required dependencies installed:
```bash
pip install requests
```

### Commands

Run the CLI from the project root:

1. **Start an exploration**:
   ```bash
   python3 cli/explorer_cli.py explore "Entropy"
   ```

2. **Retrieve an exploration graph**:
   ```bash
   python3 cli/explorer_cli.py graph 1
   ```

3. **Run API tests**:
   ```bash
   python3 cli/explorer_cli.py test
   ```
   Alternatively, use the script:
   ```bash
   ./scripts/run_api_tests.sh
   ```

## Development

The CLI can be used to verify the backend implementation.
- `cli/api_client.py`: Reusable API client.
- `cli/explorer_cli.py`: CLI interface using `argparse`.
- `cli/test_api.py`: Automated API verification.
