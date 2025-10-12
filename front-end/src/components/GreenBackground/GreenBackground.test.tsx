import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import GreenBackground from './index';

describe('GreenBackground Component', () => {
  describe('Component Unit Tests', () => {
    it('renders children content correctly', () => {
      render(
        <GreenBackground>
          <div>Test Content</div>
        </GreenBackground>
      );
      
      expect(screen.getByText('Test Content')).toBeInTheDocument();
    });

    it('applies green-background class', () => {
      const { container } = render(
        <GreenBackground>
          <span>Content</span>
        </GreenBackground>
      );
      
      const backgroundElement = container.querySelector('.green-background');
      expect(backgroundElement).toBeInTheDocument();
    });

    it('renders with multiple children', () => {
      render(
        <GreenBackground>
          <h1>Title</h1>
          <p>Paragraph</p>
          <button>Button</button>
        </GreenBackground>
      );
      
      expect(screen.getByText('Title')).toBeInTheDocument();
      expect(screen.getByText('Paragraph')).toBeInTheDocument();
      expect(screen.getByRole('button')).toBeInTheDocument();
    });

    it('renders with complex nested children', () => {
      render(
        <GreenBackground>
          <div>
            <section>
              <article>Nested content</article>
            </section>
          </div>
        </GreenBackground>
      );
      
      expect(screen.getByText('Nested content')).toBeInTheDocument();
    });

    it('renders with empty children', () => {
      const { container } = render(
        <GreenBackground>
          {''}
        </GreenBackground>
      );
      
      const backgroundElement = container.querySelector('.green-background');
      expect(backgroundElement).toBeInTheDocument();
    });

    it('renders as a div element', () => {
      const { container } = render(
        <GreenBackground>
          Content
        </GreenBackground>
      );
      
      const backgroundElement = container.firstChild;
      expect(backgroundElement).toBeInstanceOf(HTMLDivElement);
    });
  });
});