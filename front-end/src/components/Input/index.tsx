'use client'
import React, { useState } from 'react';
import './index.css';

const ChatInput: React.FC = () => {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim()) {
      console.log('Send:', message);
      setMessage('');
    }
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        className="chat-field"
        placeholder="Type a message..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button className="send-button" onClick={handleSend}>
        Enviar
      </button>
    </div>
  );
};

export default ChatInput;
