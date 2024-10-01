import React, { useState } from 'react';
import NeuralNetwork from './components/NeuralNetwork';
import UserInput from './components/UserInput';
import ArchitectureSelection from './components/ArchitectureSelection';
import './styles.css'; // Ensure this file is used for global styles

function App() {
  const [inputValues, setInputValues] = useState({
    input1: 0,
    input2: 0,
    input3: 0
  });

  const [architecture, setArchitecture] = useState('FCNN'); // Default architecture

  return (
    <div className="App">
      <header className="t">
        <h1>Welcome to NN VISION</h1>
      </header>

      <section id="visualizer" className="visualizer-section">
        <ArchitectureSelection setArchitecture={setArchitecture} />
        <NeuralNetwork inputValues={inputValues} architecture={architecture} />
      </section>

      <section id="about" className="about-section">
        <h2>About NN VISION</h2>
        <p>NN VISION is a web-based tool designed to help visualize neural networks in action. It provides an interactive interface to explore various neural network architectures, including Fully Connected Neural Networks (FCNN), Convolutional Neural Networks (CNN), and more.</p>
        <h3>What is a Neural Network?</h3>
        <p>A neural network is a computational model inspired by the way biological neural networks in the human brain process information. Neural networks consist of layers of interconnected nodes (neurons) that can learn to recognize patterns and make decisions based on input data.</p>
        
        <h3>Types of Neural Networks:</h3>
        <ul>
          <li><strong>Fully Connected Neural Network (FCNN):</strong> Every neuron in one layer is connected to every neuron in the next layer.</li>
          <li><strong>Convolutional Neural Network (CNN):</strong> Primarily used for image processing, CNNs utilize convolutional layers to automatically extract features from images.</li>
          <li><strong>Recurrent Neural Network (RNN):</strong> RNNs are designed for sequential data, making them ideal for tasks like language modeling and time series prediction.</li>
          <li><strong>Generative Adversarial Network (GAN):</strong> A type of neural network used for generating new data samples, such as images or music, by pitting two networks against each other.</li>
        </ul>

        <h3>Applications of Neural Networks:</h3>
        <ul>
          <li>Image and Speech Recognition</li>
          <li>Natural Language Processing</li>
          <li>Medical Diagnosis</li>
          <li>Financial Forecasting</li>
          <li>Game Playing and Robotics</li>
        </ul>
        
        <h3>How NN VISION Works:</h3>
        <p>Users can input values into the neural network, choose an architecture, and visualize how data flows through different layers. The tool allows for real-time calculations and adjustments, making it a valuable resource for understanding neural network dynamics.</p>
      </section>
    </div>
  );
}

export default App;
