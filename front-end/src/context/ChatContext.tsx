import React, { createContext, useContext, useState, ReactNode } from 'react';

export type Message = {
  role: 'user' | 'system';
  content: string;
};

interface ChatContextType {
  messages: Message[];
  loading: boolean;
  sendMessage: (content: string) => Promise<void>;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider = ({ children }: { children: ReactNode }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (content: string) => {
    setLoading(true);
    const newMessages: Message[] = [...messages, { role: 'user' as const, content }];
    setMessages(newMessages);
    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages: newMessages }),
      });
      const data = await response.json();
      if (data.response) {
        setMessages([...newMessages, { role: 'system' as const, content: data.response }]);
      }
    } catch {
      // Optionally handle error
    } finally {
      setLoading(false);
    }
  };

  return (
    <ChatContext.Provider value={{ messages, loading, sendMessage }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};
