# AI Internet Rabbit Hole Explorer - Copilot Instructions

## Project Overview
This is an AI-driven concept exploration engine that generates interactive knowledge graphs. Users start with a topic, and the system uses Gemini AI to expand it into related concepts, visualized as a graph with nodes (concepts) and edges (relationships).

**Tech Stack:**
- Backend: FastAPI (Python) with SQLAlchemy ORM and Pydantic schemas
- Database: PostgreSQL
- AI: Google Gemini 1.5 Flash for concept generation
- Search: Tavily API for contextual web search
- CLI: Python argparse-based tool for testing and interaction

## Architecture & Data Flow
- **Explorations**: Top-level sessions storing seed topics
- **Nodes**: Individual concepts with titles and optional summaries
- **Edges**: Directed relationships between nodes with depth levels
- **Flow**: Topic → Tavily search → Gemini prompt → Parse JSON → Save graph → Return exploration ID

## Key Patterns & Conventions

### API Structure
- Endpoints in `app/api/v1/endpoints/` (e.g., `exploration.py`)
- Schemas in `app/schemas/` with Pydantic models (e.g., `ExplorationRequest`, `ExplorationGraphResponse`)
- Services in `app/services/` handle business logic (e.g., `exploration_service.py`)
- Integrations in `app/integrations/` for external APIs (e.g., `gemini.py`, `tavily.py`)

### Database Models
- Use SQLAlchemy declarative base from `app/models/exploration.py`
- Relationships: `Exploration.nodes`, `Node.outgoing_edges`/`incoming_edges`
- Foreign keys with CASCADE delete for referential integrity
- Example: `exploration_service.generate_rabbit_hole()` creates root node + 5 concept nodes + edges

### AI Integration
- Gemini: Structured JSON prompts for concept lists (see `_build_prompt()`)
- Tavily: `get_search_context()` provides web context for better AI responses
- Error handling: Fallback to text parsing if JSON fails

### CLI Usage
- Run from project root: `python3 cli/explorer_cli.py explore "Topic"`
- Retrieve graphs: `python3 cli/explorer_cli.py graph <id>`
- Test API: `python3 cli/explorer_cli.py test` (runs `cli/test_api.py`)

### Configuration
- Environment variables in `.env`: `DATABASE_URL`, `GEMINI_API_KEY`, `TAVILY_API_KEY`
- Settings in `app/core/config.py` with automatic postgres URL conversion
- Database session via `app/db/session.py` dependency injection

### Development Workflow
- Install: `pip install -r backend/requirements.txt`
- Run backend: `uvicorn app.main:app --reload` (from backend/ directory)
- Health check: `GET /health`
- API tests validate graph structure (nodes/edges consistency)

## Common Tasks
- **Add new endpoint**: Create schema in `schemas/`, service method, endpoint in `endpoints/`, include router in `api.py`
- **Extend AI features**: Modify prompts in service `_build_prompt()`, update parsing in `_parse_response()`
- **Database changes**: Update models, ensure relationships, run migrations if needed
- **Testing**: Use CLI `test` command or run `python3 cli/test_api.py` directly

## File Reference Examples
- Core app setup: `backend/app/main.py`
- Database models: `backend/app/models/node.py`, `edge.py`, `exploration.py`
- API endpoints: `backend/app/api/v1/endpoints/exploration.py`
- Business logic: `backend/app/services/exploration_service.py`
- External APIs: `backend/app/integrations/gemini.py`, `tavily.py`
- CLI tools: `cli/explorer_cli.py`, `api_client.py`, `test_api.py`</content>
<parameter name="filePath">/workspaces/rabbit-hole-explorer/.github/copilot-instructions.md