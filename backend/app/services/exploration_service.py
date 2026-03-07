import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.integrations.gemini import gemini_service
from app.integrations.tavily import tavily_service
from app.models.exploration import Exploration
from app.models.node import Node
from app.models.edge import Edge

class ExplorationService:
    async def generate_rabbit_hole(self, topic: str, db: Session) -> Dict[str, Any]:
        """
        Generates 5 related concepts for a given topic and persists the graph to the database.
        """
        try:
            # 1. Create a new Exploration record
            exploration = Exploration(seed_topic=topic)
            db.add(exploration)
            db.flush()  # Get exploration.id

            # 2. Generate related concepts using Tavily + Gemini
            search_context = await tavily_service.get_search_context(topic)
            prompt = self._build_prompt(topic, search_context)
            response_text = await gemini_service.generate_content(prompt)
            concepts = self._parse_response(response_text)
            
            # 3. Create a Node for the original topic
            root_node = Node(
                title=topic,
                exploration_id=exploration.id,
                summary=f"Root topic: {topic}"
            )
            db.add(root_node)
            db.flush() # Get root_node.id

            # 4. Create Nodes and Edges for each generated concept
            for concept_title in concepts[:5]:
                # Create concept node
                concept_node = Node(
                    title=concept_title,
                    exploration_id=exploration.id
                )
                db.add(concept_node)
                db.flush() # Get concept_node.id

                # 5. Create Edge connecting topic_node -> concept_node
                edge = Edge(
                    parent_node_id=root_node.id,
                    child_node_id=concept_node.id,
                    depth=1
                )
                db.add(edge)

            # 6. Commit everything to the database
            db.commit()

            # 7. Return the exploration_id and concepts
            return {
                "exploration_id": exploration.id,
                "concepts": concepts[:5]
            }

        except Exception as e:
            db.rollback()
            print(f"Error in ExplorationService.generate_rabbit_hole: {e}")
            # In production, we'd likely re-raise or handle more specifically
            raise e

    def _build_prompt(self, topic: str, context: str) -> str:
        """
        Constructs the prompt for Gemini.
        """
        return f"""
        You are an expert at exploring "rabbit holes" - deep dives into interconnected topics.
        
        Topic: {topic}
        
        Context from the internet:
        {context}
        
        Based on this topic and context, identify 5 related concepts, themes, or niche sub-topics 
        that would be fascinating for someone to explore further. These should range from 
        obvious connections to surprising, "down the rabbit hole" discoveries.
        
        Return the response ONLY as a JSON list of strings.
        Example: ["Concept 1", "Concept 2", "Concept 3", "Concept 4", "Concept 5"]
        """

    def _parse_response(self, text: str) -> List[str]:
        """
        Parses the Gemini response text into a Python list.
        """
        try:
            # Find the JSON list in the text (in case there's markdown or extra text)
            start_idx = text.find('[')
            end_idx = text.rfind(']') + 1
            if start_idx == -1 or end_idx == 0:
                return [s.strip() for s in text.split('\n') if s.strip()][:5]
            
            json_str = text[start_idx:end_idx]
            concepts = json.loads(json_str)
            
            if isinstance(concepts, list):
                return [str(c) for c in concepts]
            return []
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing Gemini response: {e}")
            return [s.strip() for s in text.split('\n') if s.strip() and len(s) < 100][:5]

    async def get_exploration_graph(self, exploration_id: int, db: Session) -> Dict[str, Any]:
        """
        Retrieves an exploration graph from the database by exploration_id.
        """
        exploration = db.query(Exploration).filter(Exploration.id == exploration_id).first()
        if not exploration:
            return None
        
        # Get all nodes in this exploration
        nodes = exploration.nodes
        node_ids = [n.id for n in nodes]
        
        # Get all edges where the parent node belongs to this exploration
        # (Assuming all edges in this graph are connected within the same exploration)
        edges = db.query(Edge).filter(Edge.parent_node_id.in_(node_ids)).all()
        
        return {
            "exploration_id": exploration.id,
            "topic": exploration.seed_topic,
            "nodes": [{"id": n.id, "title": n.title} for n in nodes],
            "edges": [{"source": e.parent_node_id, "target": e.child_node_id} for e in edges]
        }

# Instantiate for use
exploration_service = ExplorationService()
