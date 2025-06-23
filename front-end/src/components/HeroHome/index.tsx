import React from 'react';
import GreenBackground from '@/components/GreenBackground';
import Logo from '@/components/Logo';
import Input from '@/components/Input';
import './index.css';

const HeroHome: React.FC = () => {
  return (
    <GreenBackground>
      <div className="hero-home">
        <div className="hero-home-center">
          <Logo />
          <Input />
        </div>

        <footer className="hero-home-footer">
          <p>{`Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry&apos;s standard dummy text ever
          industry&apos;s standard dummy text`}</p>
        </footer>
      </div>
    </GreenBackground>
  );
};

export default HeroHome;
