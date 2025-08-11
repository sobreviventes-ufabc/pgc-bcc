'use client';
import React, { useState } from 'react';
import Image from 'next/image';

import './index.css';

interface ChatInputProps {
  onSend?: (message: string) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSend }) => {
  const [message, setMessage] = useState('');
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (message.trim()) {
      if (onSend) {
        onSend(message);
      } else {
        console.log('Send:', message);
      }
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
    }
  };

  return (
    <div className="chat-input">
      <textarea
        className="chat-field"
        placeholder="Type a message..."
        value={message}
        onChange={handleChange}
        maxLength={2000}
        aria-label="Chat message input"
        ref={textareaRef}
        style={{overflowY: textareaRef.current && textareaRef.current.scrollHeight > 200 ? 'auto' : 'hidden'}}
      />
      <button
        className="send-button"
        onClick={handleSend}
        type='button'>
        <Image
          src="/img/icon-send.svg"
          alt="Send Icon"
          width={36}
          height={33}
          priority />
      </button>
    </div>
  );
};

export default ChatInput;
