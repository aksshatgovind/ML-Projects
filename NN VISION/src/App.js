import React, { useState } from 'react';
import NeuralNetwork from './components/NeuralNetwork';
import UserInput from './components/UserInput';

function App() {
  const [inputValues, setInputValues] = useState({
    input1: 0,
    input2: 0,
    input3: 0
  });

  return (
    <div className="App">
      <NeuralNetwork inputValues={inputValues} />
      <UserInput setInputValues={setInputValues} />
    </div>
  );
}

export default App;
