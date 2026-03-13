import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createExploration } from '../services/api';

const Home = () => {
  const [topic, setTopic] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleExplore = async () => {
    if (!topic.trim()) return;
    setIsLoading(true);
    try {
      const data = await createExploration(topic);
      navigate(`/exploration/${data.exploration_id}`);
    } catch (error) {
      console.error('Error creating exploration:', error);
      alert('Failed to start exploration');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h1>Rabbit Hole Explorer</h1>
      <div style={{ marginTop: '2rem' }}>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter a topic..."
          style={{ padding: '0.5rem', width: '300px' }}
        />
        <button
          onClick={handleExplore}
          disabled={isLoading}
          style={{ marginLeft: '1rem', padding: '0.5rem 1rem' }}
        >
          {isLoading ? 'Exploring...' : 'Explore'}
        </button>
      </div>
    </div>
  );
};

export default Home;
