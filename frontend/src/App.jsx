import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Exploration from './pages/Exploration';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/exploration/:id" element={<Exploration />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
