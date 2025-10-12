import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import HeroHome from './index';

const mockSendMessage = vi.fn();
vi.mock('@/context/ChatContext', () => ({
  useChat: () => ({
    sendMessage: mockSendMessage,
  }),
}));

vi.mock('@/components/GreenBackground', () => ({
  default: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="green-background-mock">{children}</div>
  ),
}));

vi.mock('@/components/Logo', () => ({
  default: () => <div data-testid="logo-mock">Logo</div>,
}));

vi.mock('@/components/Input', () => ({
  default: ({ id, autoFocus, onSend }: { 
    id: string; 
    autoFocus?: boolean; 
    onSend?: (message: string) => void;
  }) => (
    <div data-testid="input-mock">
      <input
        id={id}
        data-autofocus={autoFocus}
        placeholder="Mock input"
        onKeyDown={(e) => {
          if (e.key === 'Enter' && onSend) {
            const target = e.target as HTMLInputElement;
            onSend(target.value);
          }
        }}
      />
    </div>
  ),
}));

describe('HeroHome Component', () => {
  beforeEach(() => {
    mockSendMessage.mockClear();
  });

  describe('Component Unit Tests', () => {
    it('renders all main components', () => {
      render(<HeroHome />);
      
      expect(screen.getByTestId('green-background-mock')).toBeInTheDocument();
      expect(screen.getByTestId('logo-mock')).toBeInTheDocument();
      expect(screen.getByTestId('input-mock')).toBeInTheDocument();
    });

    it('renders footer text correctly', () => {
      render(<HeroHome />);
      
      const footerText = screen.getByText(/Assistente virtual de Inteligência Artificial/);
      expect(footerText).toBeInTheDocument();
    });

    it('starts with visible state', () => {
      const { container } = render(<HeroHome />);
      
      const heroHomeComponent = container.querySelector('.hero-home-component');
      expect(heroHomeComponent).toBeInTheDocument();
      expect(heroHomeComponent).not.toHaveClass('hidden');
    });

    it('has correct CSS class structure', () => {
      const { container } = render(<HeroHome />);
      
      expect(container.querySelector('.hero-home-component')).toBeInTheDocument();
      expect(container.querySelector('.container')).toBeInTheDocument();
      expect(container.querySelector('.hero-home')).toBeInTheDocument();
      expect(container.querySelector('.hero-home-center')).toBeInTheDocument();
      expect(container.querySelector('.hero-home-footer')).toBeInTheDocument();
    });

    it('renders Input with correct props', () => {
      render(<HeroHome />);
      
      const input = screen.getByPlaceholderText('Mock input');
      expect(input).toHaveAttribute('id', 'home-input');
      expect(input).toHaveAttribute('data-autofocus', 'true');
    });

    it('calls sendMessage when input is submitted', async () => {
      // Mock document.getElementById for focus behavior
      const mockMainChatInput = {
        focus: vi.fn(),
      };
      Object.defineProperty(document, 'getElementById', {
        value: vi.fn().mockReturnValue(mockMainChatInput),
        writable: true,
      });

      render(<HeroHome />);
      
      const input = screen.getByPlaceholderText('Mock input');
      
      // Simulate typing and pressing Enter
      Object.defineProperty(input, 'value', {
        value: 'Test message',
        writable: true,
      });
      
      fireEvent.keyDown(input, { key: 'Enter' });
      
      expect(mockSendMessage).toHaveBeenCalledWith('Test message');
    });

    it('focuses main chat input after sending message', async () => {
      const mockMainChatInput = {
        focus: vi.fn(),
      };
      const mockGetElementById = vi.fn().mockReturnValue(mockMainChatInput);
      Object.defineProperty(document, 'getElementById', {
        value: mockGetElementById,
        writable: true,
      });

      render(<HeroHome />);
      
      const input = screen.getByPlaceholderText('Mock input');
      
      Object.defineProperty(input, 'value', {
        value: 'Test message',
        writable: true,
      });
      
      fireEvent.keyDown(input, { key: 'Enter' });
      
      expect(mockGetElementById).toHaveBeenCalledWith('main-chat-input');
      expect(mockMainChatInput.focus).toHaveBeenCalled();
    });
  });
});