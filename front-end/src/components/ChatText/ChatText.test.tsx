import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import ChatText from './index';

describe('ChatText Component', () => {
  describe('Component Unit Tests', () => {
    it('renders with children content', () => {
      render(
        <ChatText variation="sent">
          Hello World
        </ChatText>
      );
      
      expect(screen.getByText('Hello World')).toBeInTheDocument();
    });

    it('applies sent variation class correctly', () => {
      const { container } = render(
        <ChatText variation="sent">
          Sent message
        </ChatText>
      );
      
      const chatTextElement = container.querySelector('.chat-text-component');
      expect(chatTextElement).toHaveClass('chat-text-component', '--sent');
    });

    it('applies received variation class correctly', () => {
      const { container } = render(
        <ChatText variation="received">
          Received message
        </ChatText>
      );
      
      const chatTextElement = container.querySelector('.chat-text-component');
      expect(chatTextElement).toHaveClass('chat-text-component', '--received');
    });

    it('renders with complex children content', () => {
      render(
        <ChatText variation="sent">
          <div>
            <p>First paragraph</p>
            <p>Second paragraph</p>
          </div>
        </ChatText>
      );
      
      expect(screen.getByText('First paragraph')).toBeInTheDocument();
      expect(screen.getByText('Second paragraph')).toBeInTheDocument();
    });

    it('contains chat-text-container wrapper', () => {
      const { container } = render(
        <ChatText variation="received">
          Container test
        </ChatText>
      );
      
      const containerElement = container.querySelector('.chat-text-container');
      expect(containerElement).toBeInTheDocument();
      expect(containerElement).toHaveTextContent('Container test');
    });

    it('renders with empty content', () => {
      const { container } = render(
        <ChatText variation="sent">
          {''}
        </ChatText>
      );
      
      const chatTextElement = container.querySelector('.chat-text-component');
      expect(chatTextElement).toBeInTheDocument();
    });
  });
});