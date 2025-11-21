'use client';

import React from 'react';

import Header from '@/components/Header';
import ChatText from '@/components/ChatText';
import Input from '@/components/Input';
import Button from '@/components/Button';
import Modal from '@/components/Modal';
import { useChat } from '@/context/ChatContext';
import './index.css';

const MainChat: React.FC = () => {
  const { messages, loading, sendMessage } = useChat();
  const messagesEndRef = React.useRef<HTMLDivElement>(null);
  const lastMessageRef = React.useRef<HTMLDivElement>(null);
  const [modalOpen, setModalOpen] = React.useState(false);

  React.useEffect(() => {
    if (messages.length > 0 && messages[messages.length - 1].role !== 'user' && lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  const handleNewChatClick = () => setModalOpen(true);
  const handleModalCancel = () => setModalOpen(false);
  const handleModalConfirm = () => {
    setModalOpen(false);
    window.location.reload();
  };

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
                <div 
                  key={idx}
                  ref={idx === messages.length - 1 ? lastMessageRef : null}
                >
                  <ChatText
                    variation="received"
                  >
                    <span
                      dangerouslySetInnerHTML={{ __html: msg.content.replace('```html', '').replace('```', '') }}
                    />
                  </ChatText>
                </div>
              )
            ))}
            {loading && (
              <ChatText variation="received">
                ...
              </ChatText>
            )}
            <div ref={messagesEndRef} />
            {messages.some(msg => msg.role !== 'user') && (
              <div className="main-chat-new-chat-button-container">
                <Button
                  text="Novo chat"
                  onClick={handleNewChatClick}
                  variation="small"
                  icon="/img/icon-new-chat-button.svg"
                  iconAlt="Novo chat"
                  iconWidth={20}
                  iconHeight={20}
                />
              </div>
            )}
          </div>
        </div>
        <div className="main-chat-input container">
          <Input
            onSend={sendMessage}
            id="main-chat-input" />
        </div>
        <footer className="main-chat-footer container">
          O UFABChat pode cometer erros. Sempre verifique as respostas.
        </footer>
      </section>
      <Modal
        isOpen={modalOpen}
        onConfirm={handleModalConfirm}
        onCancel={handleModalCancel}
      />
    </div>
  );
};

export default MainChat;