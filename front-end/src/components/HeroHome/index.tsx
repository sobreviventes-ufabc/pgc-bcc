'use client';
import classNames from 'classnames';
import React, { useState } from 'react';
import GreenBackground from '@/components/GreenBackground';
import Logo from '@/components/Logo';
import Input from '@/components/Input';
import './index.css';

const HeroHome: React.FC = () => {
  const [isVisible, setIsVisible] = useState(true);

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
                onSend={() => setIsVisible(false)}
              />
            </div>

            <footer className="hero-home-footer">
              <p>{`Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever
              industry's standard dummy text`}</p>
            </footer>
          </div>
        </div>
      </GreenBackground>
    </div>
  );
};

export default HeroHome;
