import React, { useState, useEffect } from 'react';
import chroma from 'chroma-js';
import ColorCard from './components/ColorCard';
import ColorPicker from './components/ColorPicker';
import MoveCounter from './components/MoveCounter';
import ColorChooser from './components/ColorChooser';  // Import ColorChooser
import './styles/App.css';  // Import App.css

const App = () => {
  const [currentColor, setCurrentColor] = useState('#008080'); // Teal color
  const [targetColor, setTargetColor] = useState('#FFFFE0'); // Light yellow color
  const [remainingMoves, setRemainingMoves] = useState(20);
  const [showAnimation, setShowAnimation] = useState(false);
  const [difficulty, setDifficulty] = useState('Easy'); // Default difficulty
  const [sidebarOpen, setSidebarOpen] = useState(false); // State to manage sidebar visibility
  const [showCongrats, setShowCongrats] = useState(false); // State to show Congrats message
  const [showTryAgain, setShowTryAgain] = useState(false); // State to show "Try Again" message
  const [recentScore, setRecentScore] = useState(0); // State to track recent score
  const [bestScore, setBestScore] = useState(localStorage.getItem('bestScore') || Infinity); // Retrieve best score from local storage

  useEffect(() => {
    if (remainingMoves <= 0) {
      if (!showCongrats) {
        setShowTryAgain(true); // Show "Try Again" message
      }
    }
  }, [remainingMoves, showCongrats]);

  useEffect(() => {
    if (remainingMoves <= 0 && !showCongrats) {
      // Don't show congrats if the game is over
      setShowTryAgain(true);
    }
  }, [remainingMoves]);

  const updateScores = () => {
    const newScore = difficulty === 'Easy' ? 20 - remainingMoves :
                      difficulty === 'Medium' ? 12 - remainingMoves : 6 - remainingMoves;

    setRecentScore(newScore);

    if (newScore < bestScore) {
      setBestScore(newScore);
      localStorage.setItem('bestScore', newScore); // Save best score in local storage
    }
  };

  const calculateColorDistance = (color1, color2) => {
    const rgb1 = chroma(color1).rgb();
    const rgb2 = chroma(color2).rgb();
    
    return Math.sqrt(
      Math.pow(rgb1[0] - rgb2[0], 2) +
      Math.pow(rgb1[1] - rgb2[1], 2) +
      Math.pow(rgb1[2] - rgb2[2], 2)
    );
  };

  const handleModeChange = (mode) => {
    setDifficulty(mode);
    switch (mode) {
      case 'Easy':
        setRemainingMoves(20);
        break;
      case 'Medium':
        setRemainingMoves(12);
        break;
      case 'Difficult':
        setRemainingMoves(6);
        break;
      default:
        setRemainingMoves(20);
    }
    setShowCongrats(false); // Hide Congrats message when changing difficulty
    setShowTryAgain(false); // Hide "Try Again" message
    setSidebarOpen(false); // Close the sidebar when a mode is selected
  };

  const COLOR_TOLERANCE = 15;

  const applyColorOption = (option) => {
    if (remainingMoves <= 0 || showCongrats || showTryAgain) return; // Do nothing if the game is over or options are disabled

    let newColor;
    const color = chroma(currentColor);
  
    switch (option) {
      case 'Compliment':
        newColor = color.set('hsl.h', '+180').hex();
        break;
  
      case 'Triadic+':
        newColor = color.set('hsl.h', '+120').hex();
        break;
  
      case 'Triadic-':
        newColor = color.set('hsl.h', '-120').hex();
        break;
  
      case 'Monochromatic+':
        newColor = color.set('hsl.l', '+0.1').hex();
        break;
  
      case 'Monochromatic-':
        newColor = color.set('hsl.l', '-0.1').hex();
        break;
  
      case 'Split Compliment+':
        newColor = color.set('hsl.h', '+60').hex();
        break;
  
      case 'Split Compliment-':
        newColor = color.set('hsl.h', '-60').hex();
        break;
  
      case 'Analogous+':
        newColor = color.set('hsl.h', '+30').hex();
        break;
  
      case 'Analogous-':
        newColor = color.set('hsl.h', '-30').hex();
        break;
  
      case 'Tetradic+':
        newColor = color.set('hsl.h', '+90').hex();
        break;
  
      case 'Tetradic-':
        newColor = color.set('hsl.h', '-90').hex();
        break;
  
      default:
        return;
    }
  
    setCurrentColor(newColor);
    setRemainingMoves(remainingMoves - 1);

    console.log(`Current Color: ${newColor}`);
    console.log(`Target Color: ${targetColor}`);

    // Check if the current color matches the target color
    if (calculateColorDistance(newColor, targetColor) < COLOR_TOLERANCE) {
      setShowCongrats(true);
      setShowTryAgain(false); // Hide "Try Again" message
      updateScores();
    }
  };

  const handleTitleHover = () => {
    setShowAnimation(true);
    setTimeout(() => {
      setShowAnimation(false);
    }, 2000); // Duration of the animation
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="app-container">
      <h1 onMouseEnter={handleTitleHover}>Coloria</h1>
      {showAnimation && (
        <div className="card-overlay active">
          <div
            className="color-transition-card"
            style={{
              '--start-color': currentColor,
              '--end-color': targetColor,
            }}
          >
            <div className="color-transition-text">
              Become a color master through calculated moves.
            </div>
          </div>
        </div>
      )}
      
      {/* Sidebar/NavBar */}
      <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <button className="close-btn" onClick={toggleSidebar}>x</button>
        <div className="difficulty-options">
          <button onClick={() => handleModeChange('Easy')}>Easy</button>
          <button onClick={() => handleModeChange('Medium')}>Medium</button>
          <button onClick={() => handleModeChange('Difficult')}>Difficult</button>
        </div>
        <div className="sidebar-score">
          <p>Best Score: {bestScore}</p>
        </div>

        {/* ColorChooser components */}
        <div className="color-chooser-container">
          <ColorChooser color={currentColor} onColorChange={setCurrentColor} label="Current" />
          <ColorChooser color={targetColor} onColorChange={setTargetColor} label="Target" />
        </div>
        
        <footer className="sidebar-footer">
          <p>Coloria</p>
          <p>© 2024 Aksshat Govind</p>
        </footer>
      </div>
      
      {/* Hamburger Menu Button */}
      <button className={`sidebar-toggle ${sidebarOpen ? 'hide' : ''}`} onClick={toggleSidebar}>
        <div className="bar"></div>
        <div className="bar"></div>
        <div className="bar"></div>
      </button>
      
      {/* Congrats or Try Again Message */}
      {showCongrats && (
        <div className="congrats-message">
          <h2>Congratulations!</h2>
          <p>You reached the target color!</p>
          <p>Your score: {difficulty === 'Easy' ? 20 - remainingMoves :
                          difficulty === 'Medium' ? 12 - remainingMoves : 6 - remainingMoves}</p>
        </div>
      )}

      {showTryAgain && (
        <div className="try-again-message">
          <h2>Try Again!</h2>
          <p>No more moves left</p>
        </div>
      )}

      <div className="color-cards">
        <ColorCard title="Current" color={currentColor} />
        <ColorCard title="Target" color={targetColor} />
      </div>
      <MoveCounter remainingMoves={remainingMoves} />
      <ColorPicker onOptionSelect={applyColorOption} disabled={showCongrats || showTryAgain} />
    </div>
  );
};

export default App;
