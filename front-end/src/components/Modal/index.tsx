import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import Button from '../Button';
import './Modal.css';

interface ModalProps {
  isOpen: boolean;
  onConfirm: () => void;
  onCancel?: () => void;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onConfirm, onCancel }) => {
  const [isVisible, setIsVisible] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
      setTimeout(() => setIsAnimating(true), 10);
    } else if (isVisible) {
      setIsAnimating(false);
      setTimeout(() => setIsVisible(false), 300);
    }
  }, [isOpen, isVisible]);

  if (!isVisible) return null;

  return (
    <div 
      className={`modal-overlay ${isAnimating ? 'modal-fade-in' : 'modal-fade-out'}`}
      onClick={onCancel}
    >
      <div 
        className={`modal-content ${isAnimating ? 'modal-content-fade-in' : 'modal-content-fade-out'}`}
        onClick={(e) => e.stopPropagation()}
      >
        <button 
          className="modal-close-button" 
          onClick={onCancel}
          type="button"
        >
          <Image 
            src="/img/icon-close.svg" 
            alt="Fechar"
            width={24}
            height={24}
          />
        </button>
        <h2 className="modal-title">Iniciar uma nova conversa?</h2>
        <p className="modal-message">
          A conversa atual será excluída permanentemente.
          <br />
          <br />
          Deseja continuar?
        </p>
        <div className="modal-actions">
          <Button 
            text="Confirmar" 
            onClick={onConfirm} 
            variation="small" 
          />
        </div>
      </div>
    </div>
  );
};

export default Modal;