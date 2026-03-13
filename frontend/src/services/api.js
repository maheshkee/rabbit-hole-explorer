const BASE_URL = 'http://localhost:8000/api/v1';

export const createExploration = async (topic) => {
  const response = await fetch(`${BASE_URL}/explore`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ topic }),
  });
  if (!response.ok) {
    throw new Error('Failed to create exploration');
  }
  return response.json();
};

export const getExplorationGraph = async (exploration_id) => {
  const response = await fetch(`${BASE_URL}/explorations/${exploration_id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch exploration graph');
  }
  return response.json();
};

export const expandNode = async (node_id) => {
  const response = await fetch(`${BASE_URL}/nodes/${node_id}/expand`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) {
    throw new Error('Failed to expand node');
  }
  return response.json();
};
