import React, { useRef } from 'react';
import '../styles/ColorChooser.css';  // Import ColorChooser.css

const ColorChooser = ({ color, onColorChange, label }) => {
  const colorInputRef = useRef(null);

  const handleColorChange = (event) => {
    onColorChange(event.target.value);
  };

  const handleBoxClick = () => {
    if (colorInputRef.current) {
      colorInputRef.current.click();  // Programmatically open the color picker
    }
  };

  return (
    <div className="color-chooser">
      <div className="color-box-container">
        <div 
          className="color-box" 
          style={{ backgroundColor: color }} 
          onClick={handleBoxClick}  // Handle box click
        ></div>
        <input
          type="color"
          id={`color-picker-${label.toLowerCase()}`}
          value={color}
          onChange={handleColorChange}
          className="color-picker"
          ref={colorInputRef}  // Ref for color input
        />
      </div>
      <label htmlFor={`color-picker-${label.toLowerCase()}`}>{label} Color</label>
    </div>
  );
};

export default ColorChooser;
