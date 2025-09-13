'use client';

import Header from '@/components/Header';
import ChatText from '@/components/ChatText';
import Input from '@/components/Input';
import { useChat } from '@/context/ChatContext';
import './index.css';

const MainChat: React.FC = () => {
        const { messages, loading, sendMessage } = useChat();
        return (
                <div className="main-chat-component">
                        <Header 
                          onNewChatClick={() => window.location.reload()}
                        />
                        <section className="main-chat-area">
                                <div className="main-chat-messages-scroll">
                                        <div className="main-chat-messages container">
                                                {messages.map((msg, idx) => (
                                                    <ChatText
                                                      key={idx}
                                                      variation={msg.role === 'user' ? 'sent' : 'received'}>
                                                        {msg.content}
                                                    </ChatText>
                                                ))}
                                                {loading && (
                                                    <ChatText variation="received">
                                                        ...
                                                    </ChatText>
                                                )}
                                        </div>
                                </div>
                                <div className="main-chat-input container">
                                        <Input onSend={sendMessage} />
                                </div>
                                <footer className="main-chat-footer container">
                                        AI-generated, for reference only
                                </footer>
                        </section>
                </div>
        );
};

export default MainChat;