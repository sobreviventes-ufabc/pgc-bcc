'use client';

import React from 'react';

import Header from '@/components/Header';
import ChatText from '@/components/ChatText';
import Input from '@/components/Input';
import Button from '@/components/Button';
import Modal from '@/components/Modal';
import { useChat } from '@/context/ChatContext';
import './index.css';

const loadingMessages = [
  'Buscando nos documentos oficiais',
  'Investigando documentos institucionais',
  'Lendo arquivos da UFABC',
  'Analisando informações acadêmicas',
  'Consultando registros da universidade'
];

const MainChat: React.FC = () => {
  const { messages, loading, sendMessage } = useChat();
  const messagesEndRef = React.useRef<HTMLDivElement>(null);
  const lastMessageRef = React.useRef<HTMLDivElement>(null);
  const [modalOpen, setModalOpen] = React.useState(false);
  const [loadingMessage, setLoadingMessage] = React.useState('');
  const [dots, setDots] = React.useState('');

  React.useEffect(() => {
    if (loading) {
      // Set initial random message
      setLoadingMessage(loadingMessages[Math.floor(Math.random() * loadingMessages.length)]);
      
      // Change message every 5 seconds
      const messageInterval = setInterval(() => {
        setLoadingMessage(loadingMessages[Math.floor(Math.random() * loadingMessages.length)]);
      }, 5000);

      // Animate dots every 500ms
      let dotCount = 0;
      const dotsInterval = setInterval(() => {
        dotCount = (dotCount + 1) % 4;
        setDots('.'.repeat(dotCount));
      }, 500);

      return () => {
        clearInterval(messageInterval);
        clearInterval(dotsInterval);
      };
    }
  }, [loading]);

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
                    {msg.isError ? (
                      <span>{msg.content}</span>
                    ) : (
                      <span
                        dangerouslySetInnerHTML={{ __html: msg.content.replace('```html', '').replace('```', '') }}
                      />
                    )}
                  </ChatText>
                </div>
              )
            ))}
            {loading && (
              <ChatText variation="loading">
                {loadingMessage}{dots}
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