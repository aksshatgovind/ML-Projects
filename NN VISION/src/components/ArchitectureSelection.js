import React from 'react';

function ArchitectureSelection({ setArchitecture }) {
  const handleArchitectureChange = (e) => {
    setArchitecture(e.target.value);
  };

  return (
    <div className="architecture-selection">
      <h3>Select Architecture</h3>
      <select className="architecture-dropdown" onChange={handleArchitectureChange}>
        <option value="FCNN">Fully Connected Neural Network (FCNN)</option>
        <option value="LeNet">LeNet</option>
        <option value="AlexNet">AlexNet</option>
      </select>
    </div>
  );
}

export default ArchitectureSelection;
