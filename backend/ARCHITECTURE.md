# AI Internet Rabbit Hole Explorer - System Architecture

## Overview
A full-stack application designed for guided AI exploration of complex topics. The system follows a decoupled architecture with a focus on real-time graph visualization and persistent data storage.

## Tech Stack
* **Frontend:** Next.js (React), React Flow (Graph Visualization), Tailwind CSS (Styling)
* **Backend:** FastAPI (Python), SQLAlchemy (ORM), Pydantic (Data Validation)
* **Database:** PostgreSQL (Relational Data)
* **AI Engine:** Gemini API (Concept Generation & Summarization)

## Component Roles

### 1. Frontend (Next.js)
* **Interactive Graph:** Renders the exploration path as a dynamic, zoomable 2D/3D map.
* **Navigation Logic:** Tracks the user's "Breadcrumb" trail and handles the visual expansion of nodes.
* **User Interface:** Provides the input for "Seed Topics" and sidebars for node-specific summaries.

### 2. Backend (FastAPI)
* **API Endpoints:** Handles graph generation requests, session management, and node expansion.
* **AI Orchestration:** Constructing structured prompts for Gemini and parsing the output into a graph-compatible JSON format.
* **Data Layer:** Manages CRUD operations for exploration sessions and individual node metadata.

### 3. Database (PostgreSQL)
* **Schema Design:** 
    * `Exploration`: Stores high-level session data (Title, Seed Topic, Created At).
    * `Nodes`: Stores individual concepts, their AI-generated summaries, and fun facts.
    * `Edges`: Defines the relationships and "depth" between nodes in the graph.
* **Caching:** Reuses previously generated nodes for common topics to reduce API latency and cost.

## AI Integration Flow
1. **Trigger:** User clicks a node to "dive deeper."
2. **Prompting:** Backend sends the current node context + exploration history to Gemini.
3. **Generation:** Gemini generates 4-6 semantically related but diverse sub-concepts in JSON format.
4. **Processing:** Backend validates the JSON, saves new nodes/edges to PostgreSQL, and returns them to the Frontend.
5. **Update:** Frontend performs a "Force-Directed" layout update to animate the arrival of new concepts.
