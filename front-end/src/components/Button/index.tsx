import React from 'react';
import Image from 'next/image';
import './Button.css';

interface ButtonProps {
  text: string;
  onClick: () => void;
  variation?: 'small' | 'default';
  icon?: string;
  iconAlt?: string;
  iconWidth?: number;
  iconHeight?: number;
}

const Button: React.FC<ButtonProps> = ({ 
  text, 
  onClick, 
  variation = 'default',
  icon,
  iconAlt = '',
  iconWidth = 16,
  iconHeight = 16
}) => {
  return (
    <button
      className={`button-component ${variation}`}
      onClick={onClick}
      type="button"
    >
      {text}
      {icon && (
        <Image
          src={icon}
          alt={iconAlt}
          width={iconWidth}
          height={iconHeight}
          className="button-icon"
        />
      )}
    </button>
  );
};

export default Button;
