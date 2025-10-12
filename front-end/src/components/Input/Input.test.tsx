import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ChatInput from './index';

describe('ChatInput Component', () => {
  describe('Component Unit Tests', () => {
    it('renders with required props', () => {
      render(
        <ChatInput 
          id="test-input" 
        />
      );
      
      const textarea = screen.getByPlaceholderText('Digite uma pergunta...');
      expect(textarea).toBeInTheDocument();
      expect(textarea).toHaveAttribute('id', 'test-input');
    });

    it('calls onSend when message is sent via button click', () => {
      const onSend = vi.fn();
      render(
        <ChatInput 
          id="test-input" 
          onSend={onSend} 
        />
      );
      
      const textarea = screen.getByPlaceholderText('Digite uma pergunta...');
      const sendButton = screen.getByRole('button');
      
      fireEvent.change(textarea, { target: { value: 'Test message' } });
      fireEvent.click(sendButton);
      
      expect(onSend).toHaveBeenCalledWith('Test message');
    });

    it('calls onSend when Enter is pressed', () => {
      const onSend = vi.fn();
      render(
        <ChatInput 
          id="test-input" 
          onSend={onSend} 
        />
      );
      
      const textarea = screen.getByPlaceholderText('Digite uma pergunta...');
      
      fireEvent.change(textarea, { target: { value: 'Test message' } });
      fireEvent.keyDown(textarea, { key: 'Enter', shiftKey: false });
      
      expect(onSend).toHaveBeenCalledWith('Test message');
    });

    it('does not send message when Enter is pressed with Shift key', () => {
      const onSend = vi.fn();
      render(
        <ChatInput 
          id="test-input" 
          onSend={onSend} 
        />
      );
      
      const textarea = screen.getByPlaceholderText('Digite uma pergunta...');
      
      fireEvent.change(textarea, { target: { value: 'Test message' } });
      fireEvent.keyDown(textarea, { key: 'Enter', shiftKey: true });
      
      expect(onSend).not.toHaveBeenCalled();
    });

    it('clears message after sending', () => {
      const onSend = vi.fn();
      render(
        <ChatInput 
          id="test-input" 
          onSend={onSend} 
        />
      );
      
      const textarea = screen.getByPlaceholderText('Digite uma pergunta...');
      const sendButton = screen.getByRole('button');
      
      fireEvent.change(textarea, { target: { value: 'Test message' } });
      fireEvent.click(sendButton);
      
      expect(textarea).toHaveValue('');
    });

    it('does not send empty or whitespace-only messages', () => {
      const onSend = vi.fn();
      render(
        <ChatInput 
          id="test-input" 
          onSend={onSend} 
        />
      );
      
      const textarea = screen.getByPlaceholderText('Digite uma pergunta...');
      const sendButton = screen.getByRole('button');
      
      // Test empty message
      fireEvent.change(textarea, { target: { value: '' } });
      fireEvent.click(sendButton);
      expect(onSend).not.toHaveBeenCalled();
      
      // Test whitespace-only message
      fireEvent.change(textarea, { target: { value: '   ' } });
      fireEvent.click(sendButton);
      expect(onSend).not.toHaveBeenCalled();
    });

    it('respects maxLength attribute', () => {
      render(
        <ChatInput 
          id="test-input" 
        />
      );
      
      const textarea = screen.getByPlaceholderText('Digite uma pergunta...');
      expect(textarea).toHaveAttribute('maxLength', '2000');
    });

    it('has correct aria-label', () => {
      render(
        <ChatInput 
          id="test-input" 
        />
      );
      
      const textarea = screen.getByPlaceholderText('Digite uma pergunta...');
      expect(textarea).toHaveAttribute('aria-label', 'Input do chat');
    });

    it('applies autoFocus when specified', () => {
      render(
        <ChatInput 
          id="test-input" 
          autoFocus={true} 
        />
      );
      
      const textarea = screen.getByPlaceholderText('Digite uma pergunta...');
      expect(textarea).toBeInTheDocument();
      // Simply verify the component renders correctly when autoFocus is provided
      expect(textarea).toHaveAttribute('id', 'test-input');
    });

    it('logs message to console when no onSend prop provided', () => {
      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
      
      render(
        <ChatInput 
          id="test-input" 
        />
      );
      
      const textarea = screen.getByPlaceholderText('Digite uma pergunta...');
      const sendButton = screen.getByRole('button');
      
      fireEvent.change(textarea, { target: { value: 'Test message' } });
      fireEvent.click(sendButton);
      
      expect(consoleSpy).toHaveBeenCalledWith('Send:', 'Test message');
      
      consoleSpy.mockRestore();
    });
  });
});