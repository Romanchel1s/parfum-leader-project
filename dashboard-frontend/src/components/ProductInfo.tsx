import React, { useState } from 'react';
import apiClient from '../api/apiClient';
interface ProductData {
  totalFound: number;
  totalSent: number;
  shipmentDates: { date: string; found: number; sent: number }[];
}

const ProductInfo: React.FC = () => {
  const [data, setData] = useState<ProductData | null>(null);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const fetchProductInfo = () => {
    apiClient.getProductInfo(startDate, endDate)
      .then(response => setData(response.data))
      .catch(error => console.error('Error fetching product info:', error));
  };

  return (
    <div>
      <h3>Product Info</h3>
      <input
        type="date"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
      />
      <input
        type="date"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
      />
      <button onClick={fetchProductInfo}>Fetch Info</button>
      {data && (
        <div>
          <p>Total Found: {data.totalFound}</p>
          <p>Total Sent: {data.totalSent}</p>
          <ul>
            {data.shipmentDates.map(date => (
              <li key={date.date}>
                {date.date}: Found {date.found}, Sent {date.sent}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ProductInfo;
