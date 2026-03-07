import requests
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000/api/v1"
ROOT_URL = "http://127.0.0.1:8000"

def get_health() -> Dict[str, Any]:
    """GET /health"""
    url = f"{ROOT_URL}/health"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def create_exploration(topic: str) -> Dict[str, Any]:
    """POST /api/v1/explore"""
    url = f"{BASE_URL}/explore"
    payload = {"topic": topic}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def get_exploration_graph(exploration_id: int) -> Dict[str, Any]:
    """GET /api/v1/explorations/{id}"""
    url = f"{BASE_URL}/explorations/{exploration_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
