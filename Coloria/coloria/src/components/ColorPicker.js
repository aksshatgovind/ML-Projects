import React from 'react';
import '../styles/ColorPicker.css';  // Import updated ColorPicker.css

const ColorPicker = ({ onOptionSelect }) => {
  return (
    <div className="color-picker">
      <div className="color-group">
        <div className="group-title">Compliment</div>
        <button
          onClick={() => onOptionSelect('Compliment')}
          className="color-option"
        >
          Compliment
        </button>
      </div>

      <div className="color-group">
        <div className="group-title">Triadic</div>
        <button
          onClick={() => onOptionSelect('Triadic+')}
          className="color-option"
        >
          Triadic +
        </button>
        <button
          onClick={() => onOptionSelect('Triadic-')}
          className="color-option"
        >
          Triadic -
        </button>
      </div>

      <div className="color-group">
        <div className="group-title">Monochromatic</div>
        <button
          onClick={() => onOptionSelect('Monochromatic+')}
          className="color-option"
        >
          Monochromatic +
        </button>
        <button
          onClick={() => onOptionSelect('Monochromatic-')}
          className="color-option"
        >
          Monochromatic -
        </button>
      </div>

      <div className="color-group">
        <div className="group-title">Split Compliment</div>
        <button
          onClick={() => onOptionSelect('Split Compliment+')}
          className="color-option"
        >
          Split Compliment +
        </button>
        <button
          onClick={() => onOptionSelect('Split Compliment-')}
          className="color-option"
        >
          Split Compliment -
        </button>
      </div>

      <div className="color-group">
        <div className="group-title">Analogous</div>
        <button
          onClick={() => onOptionSelect('Analogous+')}
          className="color-option"
        >
          Analogous +
        </button>
        <button
          onClick={() => onOptionSelect('Analogous-')}
          className="color-option"
        >
          Analogous -
        </button>
      </div>

      <div className="color-group">
        <div className="group-title">Tetradic</div>
        <button
          onClick={() => onOptionSelect('Tetradic+')}
          className="color-option"
        >
          Tetradic +
        </button>
        <button
          onClick={() => onOptionSelect('Tetradic-')}
          className="color-option"
        >
          Tetradic -
        </button>
      </div>
    </div>
  );
};

export default ColorPicker;
