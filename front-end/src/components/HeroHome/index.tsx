import React from 'react';
import GreenBackground from '@/components/GreenBackground';
import Logo from '@/components/Logo';
import Input from '@/components/Input';
import './index.css';

const HeroHome: React.FC = () => {
  return (
    <div className="hero-home-component">
      <GreenBackground>
        <div className="hero-home">
          <div className="hero-home-center">
            <Logo />
            <Input />
          </div>

          <footer className="hero-home-footer">
            <p>{`Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever
            industry's standard dummy text`}</p>
          </footer>
        </div>
      </GreenBackground>
    </div>
  );
};

export default HeroHome;
