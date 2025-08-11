'use client';
import HeroHome from '@/components/HeroHome';
import  MainChat from '@/components/MainChat';

export default function Home() {
  return (
    <div >
      <main>
        <MainChat />
        <HeroHome />
      </main>
    </div>
  );
}
