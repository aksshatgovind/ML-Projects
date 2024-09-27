import React, { useState, useEffect } from 'react';

export const calculateFinalActivation = (inputValues, hiddenNodes) => {

    const sum = Object.values(inputValues).reduce((acc, val) => acc + parseFloat(val), 0);
    const weightedSum = hiddenNodes.reduce((acc, node) => acc + (parseFloat(node.weight) * node.value), 0);

    const activation = Math.max(0, weightedSum);
  
    return activation;
  };
  
  