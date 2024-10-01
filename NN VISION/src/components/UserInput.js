import React from 'react';

function UserInput({ setInputValues }) {
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputValues(prevState => ({
      ...prevState,
      [name]: isNaN(parseInt(value)) ? 0 : parseInt(value)  // Ensure proper integer input
    }));
  };

  return (
    <div className="UserInput">
      <h2 className='text'>Input Layer</h2>
      <br />
      I1: <input type="number" name="input1" onChange={handleInputChange} /><br />
      I2: <input type="number" name="input2" onChange={handleInputChange} /><br />
      I3: <input type="number" name="input3" onChange={handleInputChange} /><br /><br />
    </div>
  );
}

export default UserInput;
