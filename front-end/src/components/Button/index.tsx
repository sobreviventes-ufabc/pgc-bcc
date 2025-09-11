import React from 'react';
import './Button.css';

interface ButtonProps {
  text: string;
  onClick: () => void;
  variation?: 'small' | 'default';
}

const Button: React.FC<ButtonProps> = ({ text, onClick, variation = 'default' }) => {
  return (
    <button
      className={`button-component ${variation}`}
      onClick={onClick}
      type="button"
    >
      {text}
    </button>
  );
};

export default Button;
