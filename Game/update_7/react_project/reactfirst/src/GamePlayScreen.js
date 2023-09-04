import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import './GamePlayScreen.css';

const GamePlayScreen = () => {
  const [score, setScore] = useState(0);
  const [timer, setTimer] = useState(0);
  const [inputValue, setInputValue] = useState('');
  const [currentPictureIndex, setCurrentPictureIndex] = useState(0);
  const [pictures, setPictures] = useState([]);
  const [gameFinished, setGameFinished] = useState(false);
  const [isGameReset, setIsGameReset] = useState(false); // New state variable to track game reset
  const [loadingNextPicture, setLoadingNextPicture] = useState(false); // Create a ref to track whether the function is in progress
  const navigate = useNavigate();
  const [imageURL, setImageURL] = useState(null); // State to store the image URL

///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    console.log('formatTime - formatting time');
    return `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
  };

  const loadPicturesFromFolder = async () => {
    try {
      const response = await fetch('http://localhost:5000/images'); // Use the correct server URL
      const data = await response.json();
      // Remove the base URL 'http://localhost:5000/images/' from each image URL
      const imageUrlsWithoutBaseUrl = data.map((url) => url.replace('http://localhost:5000/images/', ''));
      setPictures(imageUrlsWithoutBaseUrl);
    } catch (error) {
      console.error('Error reading pictures from folder', error);
    } finally {
      console.log('loadPicturesFromFolder - finished loading folder');
    }
  };

  const loadNextPicture = useCallback(() => {
          if (currentPictureIndex < pictures.length && !gameFinished) {
            const nextPicture = pictures[currentPictureIndex];
            fetch(`http://localhost:5000/images/${nextPicture}`)
            .then((response) => {
              if (!response.ok) {
                throw new Error('Failed to fetch the picture');
              }
              return response.blob();
            })
            .then((blob) => {
              const newImageURL = URL.createObjectURL(blob);

              setImageURL(newImageURL); // Update the state with the new image URL
              console.log(`next picture  = ${imageURL}, ${currentPictureIndex}`);
              document.querySelector('.screenshot').style.backgroundImage = `url(${imageURL})`;
              console.log(`About to set State: ${loadingNextPicture}`);
              setLoadingNextPicture(true); // Set the flag to true before starting
              setCurrentPictureIndex((prevIndex) => prevIndex + 1);
            })
            .catch((error) => {
              console.error('Error while fetching the picture', error);
              setLoadingNextPicture(false);
        });
      } else {
        setLoadingNextPicture(false);
        console.log('loadNextPicture - No more pictures to show');
      }
    }, [currentPictureIndex, pictures, gameFinished, loadingNextPicture, imageURL]);
  
  
  const handleConfirm = () => {
    if (inputValue.trim() === '') {
      console.log('Please enter a word before confirming.');
      return; // Exit the function if the input is empty
    }
    // Save the input as a text file with the same name as the picture
    if (currentPictureIndex < pictures.length) {
      const pictureName = pictures[currentPictureIndex]; ///////////////////////////////////////////////////////////////////////marker
      // Remove the 'http://localhost:5000/images/' part from the fileName before sending the request
      const fileNameWithoutBaseUrl = pictureName.replace('http://localhost:5000/images/', '');
  
      // Find the position of the last dot (.) in the file name
      const lastDotIndex = fileNameWithoutBaseUrl.lastIndexOf('.');
      // Extract the file name without the extension
      const fileNameWithoutExtension = lastDotIndex !== -1 ? fileNameWithoutBaseUrl.slice(0, lastDotIndex) : fileNameWithoutBaseUrl;
  
      const textFileEndpoint = `http://localhost:5000/save/${fileNameWithoutExtension}.txt`; // Use the correct server URL
     
      setScore((prevScore) => prevScore + 5);
      
      // Check if the text file already exists
      fetch(textFileEndpoint)
      .then((response) => {
        if (response.ok) {
          // If the file exists, update its content instead of creating a new file
          fetch(textFileEndpoint, {
            method: 'PUT',
            headers: {
              'Content-Type': 'text/plain',
            },
            body: inputValue,
          })
          .then((response) => {
            if (!response.ok) {
              console.error('Error updating text file', response);
            } else {
              // Load the next picture only when the game is not finished
              if (!gameFinished) {
                  setLoadingNextPicture(false)
                  loadNextPicture();
                  }
                  setInputValue('');
                }
              })
              .catch((error) => {
                console.error('Error updating text file', error);
              });
          } else {
            // If the file doesn't exist, create a new file
            fetch(textFileEndpoint, {
              method: 'POST',
              headers: {
                'Content-Type': 'text/plain',
              },
              body: inputValue,
            })
              .then((response) => {
                if (!response.ok) {
                  console.error('Error saving text file', response);
                } else {
                  // Load the next picture only when the game is not finished
                  if (!gameFinished) {
                    loadNextPicture();
                  }
                  setInputValue('');
                }
              })
              .catch((error) => {
                console.error('Error saving text file', error);
              });
          }
        })
        .catch((error) => {
          console.error('Error checking if the text file exists', error);
        });
    } 
    if (currentPictureIndex >= pictures.length) {
      // Game finished and no more pictures to show
      setGameFinished(true);
      setInputValue('');
      console.log('handleConfirm - currentPictureIndex: ', currentPictureIndex);
      console.log('handleConfirm - No more pictures to show');
    }
  };
  

  const handleRetry = () => {
    console.log('handleRetry - retry is pressed');
    setInputValue('');
  };

const handleEnd = () => {
  // Save the last picture and score to Local Storage
  if (currentPictureIndex > 0) {
    const lastPicture = pictures[currentPictureIndex-1]; // or pictures[currentPictureIndex - 1] ?? ///////////////////////////////////////////////////////////////marker
    localStorage.setItem('lastPicture', lastPicture);
    localStorage.setItem('score', score);
    console.log('handleEnd - last pic and score saved successfully');

  } else {
    // If there is no picture shown (game not started or already finished), do not save anything
    console.log('handleEnd - No pictures to show');
  }
  navigate('/');
};

const handleReset = useCallback(() => {
  setTimer(0);
  setInputValue('');
  setScore(0);
  setCurrentPictureIndex(0);
  localStorage.removeItem('lastPicture');
  localStorage.removeItem('score');
  localStorage.clear();
  setGameFinished(false);
  setIsGameReset(true); // Set the isGameReset state to true on reset
  localStorage.setItem('lastPicture', '');
  localStorage.setItem('score', '0');
  loadNextPicture(); // Load the first picture after resetting the game
  console.log('handleReset - currentPictureIndex: ', currentPictureIndex);
  console.log('handleReset - score: ', score);

}, [currentPictureIndex, score, loadNextPicture]);

///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////

useEffect(() => {
  loadPicturesFromFolder();
  loadNextPicture(); // Add this line 
  console.log('useEffect - load all pictures in folder');
}, []);

useEffect(() => {
  const timerInterval = setInterval(() => {
    setTimer((prevTimer) => prevTimer + 1);
  }, 1000);

  return () => clearInterval(timerInterval);
}, []);

useEffect(() => {
  // Load the last picture index and input value from localStorage if available
  const lastIndex = parseInt(localStorage.getItem('lastPictureIndex')) || 0;
  const savedInputValue = localStorage.getItem('inputValue') || '';
  const savedScore = parseInt(localStorage.getItem('score')) || 0;

  setScore(savedScore);
  setCurrentPictureIndex(lastIndex);
  setInputValue(savedInputValue);
  console.log('useEffect -  load the last picture index and input value from localStorage ');

}, []);

useEffect(() => { 
  // Check if the game has not finished and there are still pictures to show
  if (!gameFinished && !loadingNextPicture) {
    console.log('useEffect - if the game is not finished loadNextPicture ');
    loadNextPicture();
  }
}, [ gameFinished, loadNextPicture, loadingNextPicture]);


useEffect(() => {
  if (isGameReset) {
    setIsGameReset(false); // Reset the isGameReset state once we are here
    //loadNextPicture(); // Load the first picture after resetting the game
    console.log('useEffect - resetting game');
  }
}, [isGameReset]);

useEffect(() => {
  if (imageURL) {
    document.querySelector('.screenshot').style.backgroundImage = `url(${imageURL})`;
  }
}, [imageURL]);

///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////

  return (
    
    <div className="gameplay-container">
      <div className="score">Score: {score}</div>
      <div className="timer">Timer: {formatTime(timer)}</div>
      <div className="button-container">
        <button className="gameplay-button reset-button" onClick={handleReset}>
          Reset
        </button>
        <button className="gameplay-button retry-button" onClick={handleRetry}>
          Retry
        </button>
        <button className="gameplay-button confirm-button" onClick={handleConfirm}>
          Confirm
        </button>
        <button className="gameplay-button end-button" onClick={handleEnd}>
          End
        </button>
      </div>
      <div
        className="screenshot"
        style={{
          backgroundImage: gameFinished ? null : `url(${currentPictureIndex < pictures.length ? pictures[currentPictureIndex] : ''})`,
        }}
      >
        {/* Display the completion message only when the game is finished */}
        {gameFinished && currentPictureIndex >= pictures.length && !isGameReset && (
          <div className="completion-message">Congratulations, you have finished the book!</div>
        )}
      </div>
      <input
        type="text"
        className="input-field"
        placeholder="Enter word - أدخل الكلمة"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
      <div className="footer">
        &copy; {new Date().getFullYear()} - All Rights Reserved <br />
        Omar Salem - 900202515 & Abdelhalim Ali - 900193539 & Andrew Sinout - 900182668
      </div>
    </div>
  );
};

export default GamePlayScreen;
