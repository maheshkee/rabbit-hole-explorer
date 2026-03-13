# System Architecture

Rabbit Hole Explorer is structured as a lightweight full-stack system for generating and exploring AI-assisted knowledge graphs.

## Architecture Diagram

```text
User
  |
  v
React + Vite Frontend
  |
  v
FastAPI Backend
  |
  +--> Tavily Search
  |
  +--> Google Gemini
  |
  v
PostgreSQL
```

## Components

### Frontend

The frontend is a React application built with Vite. It is responsible for:

- collecting the initial topic from the user
- rendering exploration graphs with React Flow
- applying automatic hierarchical layout through Dagre
- supporting node clicks, drag interactions, zoom, and pan

### Backend

The backend is a FastAPI application that exposes exploration endpoints and coordinates graph generation. Its responsibilities include:

- accepting exploration and expansion requests
- validating API payloads
- orchestrating Tavily and Gemini calls
- persisting nodes, edges, and exploration metadata
- returning graph data in a frontend-friendly format

### AI Integrations

Two external AI-related services power the graph generation workflow:

- Tavily supplies web-derived context to ground topic exploration
- Google Gemini generates related concepts from the topic and search context

This combination improves the quality of graph branches by pairing live context with LLM-driven synthesis.

### Database

PostgreSQL stores:

- exploration records
- graph nodes
- graph edges

This makes each exploration persistent, queryable, and expandable over time instead of being limited to one transient AI response.

## Request Flow

1. A user enters a topic in the frontend.
2. The frontend sends the request to the FastAPI backend.
3. The backend queries Tavily for contextual search results.
4. The backend prompts Gemini to generate related concepts.
5. The backend stores the resulting exploration graph in PostgreSQL.
6. The frontend fetches the graph and renders it with automatic layout.
7. On node expansion, the same process repeats for the selected node.
