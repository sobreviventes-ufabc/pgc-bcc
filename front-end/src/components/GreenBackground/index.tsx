import React from 'react';
import './index.css';

type Props = { children: React.ReactNode };

const HeroHome: React.FC<Props> = ({ children }) => {
  return (
    <div className="green-background">
      {children}
    </div>
  );
};

export default HeroHome;
