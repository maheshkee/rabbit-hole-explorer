import json
from typing import List
from app.integrations.gemini import gemini_service
from app.integrations.tavily import tavily_service

class ExplorationService:
    async def generate_rabbit_hole(self, topic: str) -> List[str]:
        """
        Generates 5 related concepts for a given topic using Tavily for context
        and Gemini for generation.
        """
        # 1. Retrieve internet context
        search_context = await tavily_service.get_search_context(topic)
        
        # 2. Build a prompt for Gemini
        prompt = self._build_prompt(topic, search_context)
        
        # 3. Call Gemini to generate content
        try:
            response_text = await gemini_service.generate_content(prompt)
            
            # 4. Parse the output into a Python list
            concepts = self._parse_response(response_text)
            
            # 5. Return the list
            return concepts[:5]  # Ensure exactly 5 if possible, but return what we got up to 5
        except Exception as e:
            # Basic error handling - could be more sophisticated
            print(f"Error in ExplorationService.generate_rabbit_hole: {e}")
            return []

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
                # If no brackets found, try simple split or return empty
                return [s.strip() for s in text.split('\n') if s.strip()][:5]
            
            json_str = text[start_idx:end_idx]
            concepts = json.loads(json_str)
            
            if isinstance(concepts, list):
                return [str(c) for c in concepts]
            return []
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing Gemini response: {e}")
            # Fallback: simple line split if JSON fails
            return [s.strip() for s in text.split('\n') if s.strip() and len(s) < 100][:5]

# Instantiate for use
exploration_service = ExplorationService()
