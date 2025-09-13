'use client';

import HeroHome from '@/components/HeroHome';
import MainChat from '@/components/MainChat';
import { ChatProvider } from '@/context/ChatContext';

export default function Home() {
  return (
    <ChatProvider>
      <div>
        <main>
          <MainChat />
          <HeroHome />
        </main>
      </div>
    </ChatProvider>
  );
}
