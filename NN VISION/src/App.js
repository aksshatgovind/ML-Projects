import React, { useState } from 'react';
import NeuralNetwork from './components/NeuralNetwork';
import UserInput from './components/UserInput';
import ArchitectureSelection from './components/ArchitectureSelection';

function App() {
  const [inputValues, setInputValues] = useState({
    input1: 0,
    input2: 0,
    input3: 0
  });

  const [architecture, setArchitecture] = useState('FCNN'); // Default architecture

  return (
    <div className="App">
      <h1>NN VISION</h1>
      <ArchitectureSelection setArchitecture={setArchitecture} />
      <NeuralNetwork inputValues={inputValues} architecture={architecture} />
      <UserInput setInputValues={setInputValues} />
    </div>
  );
}

export default App;

