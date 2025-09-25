'use client';
import classNames from 'classnames';
import React, { useState } from 'react';
import GreenBackground from '@/components/GreenBackground';
import Logo from '@/components/Logo';
import Input from '@/components/Input';
import { useChat } from '@/context/ChatContext';
import './index.css';

const HeroHome: React.FC = () => {
  const [isVisible, setIsVisible] = useState(true);
  const { sendMessage } = useChat();

  return (
    <div
      className={classNames('hero-home-component', {'hidden': !isVisible})}
    >
      <GreenBackground>
        <div className="container">
          <div className={classNames('hero-home', {'hidden': !isVisible})}>
            <div className='hero-home-center'>
              <Logo />
                <Input 
                  id="home-input" 
                  autoFocus={true}
                  onSend={async (message: string) => {
                    setIsVisible(false);

                    const mainChatInput = document.getElementById('main-chat-input');
                    if (mainChatInput) {
                      (mainChatInput as HTMLTextAreaElement).focus();
                    }

                    await sendMessage(message);
                  }}
                />
            </div>

            <footer className="hero-home-footer">
              <p>{'Assistente virtual de Inteligência Artificial criado para apoiar os estudantes da UFABC, oferecendo respostas rápidas, confiáveis e atualizadas sobre matrícula, calendários, fretado e PGC'}</p>
            </footer>
          </div>
        </div>
      </GreenBackground>
    </div>
  );
};

export default HeroHome;
