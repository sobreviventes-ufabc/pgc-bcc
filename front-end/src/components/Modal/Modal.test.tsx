import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Modal from './index';

// Mock the Button component
vi.mock('../Button', () => ({
  default: ({ text, onClick, variation }: { 
    text: string; 
    onClick: () => void; 
    variation?: string;
  }) => (
    <button 
      onClick={onClick}
      data-testid="button-mock"
      data-variation={variation}
    >
      {text}
    </button>
  ),
}));

describe('Modal Component', () => {
  describe('Component Unit Tests', () => {
    it('does not render when isOpen is false', () => {
      render(
        <Modal 
          isOpen={false}
          onConfirm={vi.fn()}
        />
      );
      
      expect(screen.queryByText('Iniciar uma nova conversa?')).not.toBeInTheDocument();
    });

    it('renders when isOpen is true', () => {
      render(
        <Modal 
          isOpen={true}
          onConfirm={vi.fn()}
        />
      );
      
      expect(screen.getByText('Iniciar uma nova conversa?')).toBeInTheDocument();
    });

    it('renders modal title correctly', () => {
      render(
        <Modal 
          isOpen={true}
          onConfirm={vi.fn()}
        />
      );
      
      const title = screen.getByRole('heading', { level: 2 });
      expect(title).toHaveTextContent('Iniciar uma nova conversa?');
    });

    it('renders modal message correctly', () => {
      render(
        <Modal 
          isOpen={true}
          onConfirm={vi.fn()}
        />
      );
      
      expect(screen.getByText(/A conversa atual será excluída permanentemente/)).toBeInTheDocument();
      expect(screen.getByText(/Deseja continuar?/)).toBeInTheDocument();
    });

    it('calls onConfirm when confirm button is clicked', () => {
      const onConfirm = vi.fn();
      render(
        <Modal 
          isOpen={true}
          onConfirm={onConfirm}
        />
      );
      
      const confirmButton = screen.getByTestId('button-mock');
      fireEvent.click(confirmButton);
      
      expect(onConfirm).toHaveBeenCalledTimes(1);
    });

    it('calls onCancel when close button is clicked', () => {
      const onCancel = vi.fn();
      render(
        <Modal 
          isOpen={true}
          onConfirm={vi.fn()}
          onCancel={onCancel}
        />
      );
      
      const closeButton = screen.getByRole('button', { name: /Fechar/i });
      fireEvent.click(closeButton);
      
      expect(onCancel).toHaveBeenCalledTimes(1);
    });

    it('calls onCancel when overlay is clicked', () => {
      const onCancel = vi.fn();
      const { container } = render(
        <Modal 
          isOpen={true}
          onConfirm={vi.fn()}
          onCancel={onCancel}
        />
      );
      
      const overlay = container.querySelector('.modal-overlay');
      if (overlay) {
        fireEvent.click(overlay);
        expect(onCancel).toHaveBeenCalledTimes(1);
      }
    });

    it('does not call onCancel when modal content is clicked', () => {
      const onCancel = vi.fn();
      const { container } = render(
        <Modal 
          isOpen={true}
          onConfirm={vi.fn()}
          onCancel={onCancel}
        />
      );
      
      const modalContent = container.querySelector('.modal-content');
      if (modalContent) {
        fireEvent.click(modalContent);
        expect(onCancel).not.toHaveBeenCalled();
      }
    });

    it('renders confirm button with correct props', () => {
      render(
        <Modal 
          isOpen={true}
          onConfirm={vi.fn()}
        />
      );
      
      const confirmButton = screen.getByTestId('button-mock');
      expect(confirmButton).toHaveTextContent('Confirmar');
      expect(confirmButton).toHaveAttribute('data-variation', 'small');
    });

    it('has correct CSS class structure', () => {
      const { container } = render(
        <Modal 
          isOpen={true}
          onConfirm={vi.fn()}
        />
      );
      
      expect(container.querySelector('.modal-overlay')).toBeInTheDocument();
      expect(container.querySelector('.modal-content')).toBeInTheDocument();
      expect(container.querySelector('.modal-title')).toBeInTheDocument();
      expect(container.querySelector('.modal-message')).toBeInTheDocument();
      expect(container.querySelector('.modal-actions')).toBeInTheDocument();
    });

    it('renders close button with correct attributes', () => {
      render(
        <Modal 
          isOpen={true}
          onConfirm={vi.fn()}
        />
      );
      
      const closeButton = screen.getByRole('button', { name: /Fechar/i });
      expect(closeButton).toHaveAttribute('type', 'button');
      expect(closeButton).toHaveClass('modal-close-button');
    });

    it('handles missing onCancel prop gracefully', () => {
      expect(() => {
        render(
          <Modal 
            isOpen={true}
            onConfirm={vi.fn()}
          />
        );
      }).not.toThrow();
    });

    it('prevents event propagation on modal content click', () => {
      const onCancel = vi.fn();
      const { container } = render(
        <Modal 
          isOpen={true}
          onConfirm={vi.fn()}
          onCancel={onCancel}
        />
      );
      
      const modalContent = container.querySelector('.modal-content');
      if (modalContent) {
        const clickEvent = new MouseEvent('click', {
          bubbles: true,
          cancelable: true,
        });
        
        const stopPropagationSpy = vi.fn();
        Object.defineProperty(clickEvent, 'stopPropagation', {
          value: stopPropagationSpy,
        });
        
        modalContent.dispatchEvent(clickEvent);
        expect(stopPropagationSpy).toHaveBeenCalled();
      }
    });
  });
});