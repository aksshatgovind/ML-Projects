import React from 'react';
import '../styles/ColorCard.css';  // Import updated ColorCard.css

const ColorCard = ({ title, color }) => {
  return (
    <div className="color-card">
      <div className="color-card-title">{title}</div>
      <div className="color-card-inner">
        <div className="color-box" style={{ backgroundColor: color }}></div>
      </div>
    </div>
  );
};

export default ColorCard;
