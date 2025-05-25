/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useEffect, useState } from 'react';
import api from '../api/apiClient';

const EmployeeMessages: React.FC<{ employeeId: string }> = ({ employeeId }) => {
  const [messages, setMessages] = useState<any[]>([]);

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const data = await api.getEmployeeMessages(employeeId);
        setMessages(data); // Update state with fetched data
      } catch (err) {
        console.error('Error fetching messages:', err);
      }
    };

    fetchMessages();
  }, [employeeId]); // Add `employeeId` to the dependency array to avoid stale values

  return (
    <div>
      <h1>Employee Messages</h1>
      <ul>
        {messages.map(msg => (
          <li key={msg.messageId}>
            <strong>{msg.timestamp}:</strong> {msg.content}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EmployeeMessages;



