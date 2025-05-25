import React, { useState } from 'react';
import apiClient from '../api/apiClient';
const ProductFrequency: React.FC = () => {
  const [frequency, setFrequency] = useState('');
  const [status, setStatus] = useState('');

  const updateFrequency = () => {
    apiClient.updateProductFrequency(frequency)
      .then(response => setStatus(response.data.status))
      .catch(error => console.error('Error updating frequency:', error));
  };

  return (
    <div>
      <h3>Update Product Frequency</h3>
      <input
        type="text"
        placeholder="Enter new frequency"
        value={frequency}
        onChange={(e) => setFrequency(e.target.value)}
      />
      <button onClick={updateFrequency}>Update</button>
      {status && <p>Status: {status}</p>}
    </div>
  );
};

export default ProductFrequency;
