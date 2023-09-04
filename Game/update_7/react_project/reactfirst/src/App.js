import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainScreen from './MainScreen';
import GamePlayScreen from './GamePlayScreen';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/"  element={<MainScreen/>} />
        <Route path="/game_play_screen"  element={<GamePlayScreen/>} />
        {/* Add other routes if needed */}
      </Routes>
    </Router>
  );
};

export default App;
