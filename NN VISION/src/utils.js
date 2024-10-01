export const calculateFinalActivation = (inputValues, hiddenNodes) => {
  const weightedSum = hiddenNodes.reduce((acc, node) => acc + node.weight * node.value, 0);
  return Math.max(0, weightedSum);  // Using ReLU activation
};