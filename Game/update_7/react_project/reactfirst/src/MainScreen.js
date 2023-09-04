import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './MainScreen.css';

const MainScreen = () => {
  const [score, setScore] = useState(0);
  const [inputValue, setInputValue] = useState(''); // State for the input value
  const navigate = useNavigate();

  const handleStartButtonClick = () => {
    // Redirect to the game_play_screen
    navigate('/game_play_screen');
  };

  const handleInputChange = (event) => {
    // Update the inputValue state when the input field value changes
    setInputValue(event.target.value);
  };

  useEffect(() => {
    // Check if the score is available in Local Storage, otherwise set a default score
    const storedScore = parseInt(localStorage.getItem('score')) || 0;
    setScore(storedScore);
  }, []);

  return (
    <div className="main-screen">
      <h1 className="header">AUC Library OCR </h1>
      <button className="start-button" onClick={handleStartButtonClick}>
        Start
      </button>
      <div className="score">Score: {score}</div>

      {/* Input field */}
      <input
        type="text"
        placeholder="Enter folder path..."
        value={inputValue}
        onChange={handleInputChange}
      />

      <div className="footer">
        &copy; {new Date().getFullYear()} - All Rights Reserved <br />
        Omar Salem - 900202515 & Abdelhalim Ali - 900193539 & Andrew Sinout - 900182668
      </div>
    </div>
  );
};

export default MainScreen;
