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
                # Avoid duplicates within the same exploration
                existing_node = db.query(Node).filter(
                    Node.title == concept_title,
                    Node.exploration_id == exploration_id
                ).first()
                if existing_node:
                    continue

                # Create concept node
                concept_node = Node(
                    title=concept_title,
                    exploration_id=exploration_id
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

    async def expand_node(self, node_id: int, db: Session) -> Dict[str, Any]:
        """
        Expands an existing node by generating 5 more related concepts.
        """
        try:
            # 1. Retrieve node from database
            node = db.query(Node).filter(Node.id == node_id).first()
            if not node:
                raise ValueError(f"Node with ID {node_id} not found.")

            topic = node.title
            exploration_id = node.exploration_id

            # 2. Calculate correct depth for the new nodes
            parent_edge = db.query(Edge).filter(Edge.child_node_id == node_id).first()
            new_depth = (parent_edge.depth + 1) if parent_edge else 1

            # 3. Retrieve Tavily context for the node's title
            search_context = await tavily_service.get_search_context(topic)
            
            # 4. Generate 5 related concepts using Gemini
            prompt = self._build_prompt(topic, search_context)
            response_text = await gemini_service.generate_content(prompt)
            concepts = self._parse_response(response_text)

            new_node_titles = []
            
            # 5. Create new Node and Edge records
            for concept_title in concepts[:5]:
                # Avoid duplicate nodes within the same exploration
                existing_node = db.query(Node).filter(
                    Node.title == concept_title,
                    Node.exploration_id == exploration_id
                ).first()
                
                if existing_node:
                    continue

                # Create new node
                new_node = Node(
                    title=concept_title,
                    exploration_id=exploration_id
                )
                db.add(new_node)
                db.flush() # Get new_node.id
                
                # Create edge from original node to the new node
                edge = Edge(
                    parent_node_id=node_id,
                    child_node_id=new_node.id,
                    depth=new_depth
                )
                db.add(edge)
                new_node_titles.append(concept_title)

            # 6. Commit transaction
            db.commit()

            return {
                "node_id": node_id,
                "new_nodes": new_node_titles
            }

        except Exception as e:
            db.rollback()
            print(f"Error in ExplorationService.expand_node: {e}")
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
