'use client';

import React from 'react';

import Header from '@/components/Header';
import ChatText from '@/components/ChatText';
import Input from '@/components/Input';
import { useChat } from '@/context/ChatContext';
import './index.css';

const MainChat: React.FC = () => {
  const { messages, loading, sendMessage } = useChat();
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  return (
    <div className="main-chat-component">
      <Header
        onNewChatClick={() => window.location.reload()}
      />
      <section className="main-chat-area">
        <div className="main-chat-messages-scroll">
          <div className="main-chat-messages container">
            {messages.map((msg, idx) => (
              msg.role === 'user' ? (
                <ChatText
                  key={idx}
                  variation="sent"
                >
                  {msg.content}
                </ChatText>
              ) : (
                <ChatText
                  key={idx}
                  variation="received"
                >
                  <span
                    dangerouslySetInnerHTML={{ __html: msg.content.replace('```html', '').replace('```', '') }}
                  />
                </ChatText>
              )
            ))}
            {loading && (
              <ChatText variation="received">
                ...
              </ChatText>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
        <div className="main-chat-input container">
          <Input
            onSend={sendMessage}
            id="main-chat-input" />
        </div>
        <footer className="main-chat-footer container">
          O UFABChat pode cometer erros. Por isso, é bom checar as respostas.
        </footer>
      </section>
    </div>
  );
};

export default MainChat;