import React, { useState, useEffect } from 'react';
import { calculateFinalActivation } from '../utils'; 


function NeuralNetwork({ inputValues, architecture = 'FCNN' }) {
  const [hiddenNodes, setHiddenNodes] = useState([
    { id: 'hidden1', x: 300, y: 150, value: 0 },
    { id: 'hidden2', x: 300, y: 250, value: 0 },
    { id: 'hidden3', x: 300, y: 350, value: 0 },
    { id: 'hidden4', x: 300, y: 450, value: 0 },
  ]);

  const [outputNode, setOutputNode] = useState({
    id: 'output',
    x: 700,
    y: 300,
    activation: 0,
    color: 'red',
    size: 30,
  });

  const [inputNodeValues, setInputNodeValues] = useState({
    input1: 0,
    input2: 0,
    input3: 0,
  });

  const [inputToHiddenWeights, setInputToHiddenWeights] = useState(() => {
    const weights = [];
    for (let i = 0; i < 4; i++) {
      weights.push(Array(3).fill(0)); 
    }
    return weights;
  });

  const [hiddenToOutputWeights, setHiddenToOutputWeights] = useState([0.5, 0.4, -0.2, 0.1]);  // Example weights

  const [edges, setEdges] = useState([]);
  const [inputsComplete, setInputsComplete] = useState(false);
  const [outputNodeValue, setOutputNodeValue] = useState(0);

  // Customization for nodes and edges
  const [nodeSize, setNodeSize] = useState(30);
  const [edgeWidth, setEdgeWidth] = useState(2);

  // Handle node size change
  const handleNodeSizeChange = (e) => {
    setNodeSize(parseFloat(e.target.value));
  };

  // Handle edge width change
  const handleEdgeWidthChange = (e) => {
    setEdgeWidth(parseFloat(e.target.value));
  };

  const handleWeightChange = (e, j, i) => {
    const newWeight = parseFloat(e.target.value);
    setInputToHiddenWeights(prevWeights => {
      const updatedWeights = [...prevWeights];
      updatedWeights[j][i] = newWeight;
      return updatedWeights;
    });
  };

  // Generates edges between input and hidden nodes based on weights
  const generateRandomEdges = () => {
    const edges = [];
    for (let i = 0; i < hiddenNodes.length; i++) {
      const target = hiddenNodes[i].id;
      for (let j = 0; j < 3; j++) {
        const source = `input${j + 1}`;
        const weight = inputToHiddenWeights[i][j]; 
        edges.push({ source, target, weight });
      }
    }
    return edges;
  };

  const calculateHiddenNodeValue = (hiddenNode, inputNodeValues, edges) => {
    const value = edges
      .filter(edge => edge.target === hiddenNode.id)
      .reduce((acc, edge) => {
        const inputValue = inputNodeValues[edge.source];
        const weight = edge.weight;
        return acc + inputValue * weight;
      }, 0);
    return Math.max(0, value); // ReLU activation
  };

  const calculateOutputNodeValue = () => {
    const outputValue = calculateFinalActivation(inputNodeValues, hiddenNodes);
    return outputValue;
  };

  useEffect(() => {
    setInputNodeValues(inputValues);
  }, [inputValues]);

  useEffect(() => {
    if (inputsComplete) {
      const updatedHiddenNodes = hiddenNodes.map((hiddenNode, index) => {
        const value = calculateHiddenNodeValue(hiddenNode, inputNodeValues, edges);
        return { ...hiddenNode, value };
      });
      setHiddenNodes(updatedHiddenNodes);
    }
  }, [inputNodeValues, inputsComplete, edges, hiddenNodes]);

  useEffect(() => {
    setEdges(generateRandomEdges());
  }, [inputNodeValues, hiddenNodes, inputToHiddenWeights]);

  const handleInputComplete = () => {
    setInputsComplete(true);
  };

  const handleOutputCalculation = () => {
    const outputValue = calculateFinalActivation(inputNodeValues, hiddenNodes);
    setOutputNodeValue(outputValue);
  };

  return (
    <div className="NeuralNetwork">
      <div className="tt">NN VISION</div>

      {/* Node and Edge Customization Section */}
      <div className="controls">
        <label>
          Node Size:
          <input type="range" min="10" max="50" value={nodeSize} onChange={handleNodeSizeChange} />
        </label>
        <label>
          Edge Width:
          <input type="range" min="1" max="10" value={edgeWidth} onChange={handleEdgeWidthChange} />
        </label>
      </div>

      <svg width="1200" height="800">
        {/* Drawing Input to Hidden connections */}
        {[...Array(3).keys()].map((i) => (
          [...Array(4).keys()].map((j) => (
            <g key={`input-hidden-${i}-${j}`}>
              <line
                x1={130}
                y1={(i + 1) * 210}
                x2={370}
                y2={(j + 1) * 175}
                stroke="black"
                strokeWidth={edgeWidth}
                markerEnd="url(#arrowhead)"
              />
              <foreignObject x={(130 + 350) / 2 - 1} y={(i + 1) * 185 + ((j + 1) * 210 - (i + 1) * 210) / 2 - 10} width="20" height="20">
                <input
                  type="number"
                  style={{ width: "30px", height: "20px" }}
                  value={inputToHiddenWeights[j][i]} 
                  onChange={(e) => handleWeightChange(e, j, i)} 
                />
              </foreignObject>
            </g>
          ))
        ))}

        {/* Drawing Hidden to Output connections */}
        {[...Array(4).keys()].map((index) => (
          <g key={`hidden-output-${index}`}>
            <line
              x1={429}
              y1={(index + 1) * 176}
              x2={619}
              y2={400}
              stroke="black"
              strokeWidth={edgeWidth}
              markerEnd="url(#arrowhead)"
            />
            <foreignObject x={(400 + 650) / 2 - 10} y={(index + 1) * 190 + (410 - (index + 1) * 210) / 2 - 10} width="20" height="20">
              <input type="number" style={{ width: "30px", height: "20px" }} />
            </foreignObject>
          </g>
        ))}

        {/* Drawing Input Nodes */}
        {Object.keys(inputNodeValues).map((input, index) => (
          <g key={input}>
            <circle cx={100} cy={(index + 1) * 210} r={nodeSize} fill="green" opacity="0.66" />
            <text x={100} y={(index + 1) * 210} fill="white" textAnchor="middle" alignmentBaseline="central">{`I ${index + 1}`}</text>
            <text x={100} y={(index + 1) * 210 + 50} fill="black" textAnchor="middle" alignmentBaseline="central">{inputNodeValues[input]}</text>
          </g>
        ))}

        {/* Drawing Hidden Nodes */}
        {hiddenNodes.map((hiddenNode, index) => (
          <g key={hiddenNode.id}>
            <circle cx={400} cy={(index + 1) * 175} r={nodeSize} fill="blue" opacity="0.66" />
            <text x={400} y={(index + 1) * 175} fill="white" textAnchor="middle" alignmentBaseline="central">{`H${index + 1}`}</text>
            <text x={400} y={(index + 1) * 175 + 50} fill="black" textAnchor="middle" alignmentBaseline="central">{hiddenNode.value.toFixed(2)}</text>
          </g>
        ))}

        {/* Drawing Output Node */}
        <circle cx={620} cy={400} r={nodeSize} fill={outputNode.color} opacity="0.66" />
        <text x={620} y={400} fill="white" textAnchor="middle" alignmentBaseline="central">O</text>
        <text x={620} y={450} fill="black" textAnchor="middle" alignmentBaseline="central">{outputNodeValue.toFixed(2)}</text>
      </svg>

      <button className="set-button" onClick={handleInputComplete}>Set Input Weights</button>
      <button className="calc-button" onClick={handleOutputCalculation}>Calculate Output</button>

    </div>
  );
}

export default NeuralNetwork;
