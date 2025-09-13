'use client';

import Header from '@/components/Header';
import ChatText from '@/components/ChatText';
import Input from '@/components/Input';

import './index.css';

const MainChat: React.FC = () => {
    return (
        <div className="main-chat-component">
            <Header 
              onNewChatClick={() => window.location.reload()}
            />
            <section className="main-chat-area">
                <div className="main-chat-messages-scroll">
                    <div className="main-chat-messages container">
                        <ChatText variation="sent">Olá, tudo bem?</ChatText>
                        <ChatText variation="received">Oi! Como posso ajudar?</ChatText>
                        <ChatText variation="sent">Olá, tudo bem?</ChatText>
                        <ChatText variation="received">Oi! Como posso ajudar?</ChatText>
                        <ChatText variation="sent">Olá, tudo bem?</ChatText>
                        <ChatText variation="received">Oi! Como posso ajudar?</ChatText>
                        <ChatText variation="sent">Olá, tudo bem?</ChatText>
                        <ChatText variation="received">Oi! Como posso ajudar?</ChatText>
                        <ChatText variation="sent">Olá, tudo bem?</ChatText>
                        <ChatText variation="received">Oi! Como posso ajudar?</ChatText>
                        <ChatText variation="sent">Olá, tudo bem?</ChatText>
                        <ChatText variation="received">Oi! Como posso ajudar?</ChatText>
                        <ChatText variation="sent">Olá, tudo bem?</ChatText>
                        <ChatText variation="received">Oi! Como posso ajudar?</ChatText>
                    </div>
                </div>
                <div className="main-chat-input container">
                    <Input />
                </div>
                <footer className="main-chat-footer container">
                    AI-generated, for reference only
                </footer>
            </section>
        </div>
    );
};

export default MainChat;