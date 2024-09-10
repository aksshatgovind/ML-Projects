import React from 'react';
import '../styles/MoveCounter.css';  // Import MoveCounter.css

const MoveCounter = ({ remainingMoves }) => {
  return (
    <div className="move-counter">
      <p>Remaining Moves: {remainingMoves}</p>
    </div>
  );
};

export default MoveCounter;

