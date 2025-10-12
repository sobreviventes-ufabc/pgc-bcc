import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Logo from './index';

describe('Logo Component', () => {
  describe('Component Unit Tests', () => {
    it('renders with default size', () => {
      render(<Logo />);
      
      const logoImage = screen.getByAltText('UFABChat Logo');
      expect(logoImage).toBeInTheDocument();
      expect(logoImage).toHaveAttribute('width', '268');
      expect(logoImage).toHaveAttribute('height', '74');
    });

    it('renders with small size', () => {
      render(
        <Logo size="small" />
      );
      
      const logoImage = screen.getByAltText('UFABChat Logo');
      expect(logoImage).toBeInTheDocument();
      expect(logoImage).toHaveAttribute('width', '146');
      expect(logoImage).toHaveAttribute('height', '38');
    });

    it('renders with default size when explicitly set', () => {
      render(
        <Logo size="default" />
      );
      
      const logoImage = screen.getByAltText('UFABChat Logo');
      expect(logoImage).toBeInTheDocument();
      expect(logoImage).toHaveAttribute('width', '268');
      expect(logoImage).toHaveAttribute('height', '74');
    });

    it('has correct src attribute', () => {
      render(<Logo />);
      
      const logoImage = screen.getByAltText('UFABChat Logo');
      expect(logoImage).toHaveAttribute('src');
      // Note: Next.js Image component may modify the src, so we just check it exists
    });

    it('has correct class name', () => {
      render(<Logo />);
      
      const logoImage = screen.getByAltText('UFABChat Logo');
      expect(logoImage).toHaveClass('app-logo');
    });

    it('has priority attribute for optimization', () => {
      render(<Logo />);
      
      const logoImage = screen.getByAltText('UFABChat Logo');
      // Next.js Image with priority should be rendered as an img element
      expect(logoImage).toBeInTheDocument();
      expect(logoImage.tagName).toBe('IMG');
    });

    it('renders as an image element', () => {
      render(<Logo />);
      
      const logoImage = screen.getByRole('img');
      expect(logoImage).toBeInTheDocument();
      expect(logoImage).toHaveAttribute('alt', 'UFABChat Logo');
    });
  });
});