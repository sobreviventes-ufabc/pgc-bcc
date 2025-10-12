import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './index';

describe('Button Component', () => {
  describe('Component Unit Tests', () => {
    it('renders with provided text', () => {
      const onClick = vi.fn();
      render(
        <Button 
          text="Test Button" 
          onClick={onClick} 
        />
      );
      
      expect(screen.getByText('Test Button')).toBeInTheDocument();
      expect(screen.getByRole('button')).toBeInTheDocument();
    });

    it('calls onClick when clicked', () => {
      const onClick = vi.fn();
      render(
        <Button 
          text="Clickable Button" 
          onClick={onClick} 
        />
      );
      
      const button = screen.getByRole('button');
      fireEvent.click(button);
      
      expect(onClick).toHaveBeenCalledTimes(1);
    });

    it('applies default variation class when no variation provided', () => {
      const onClick = vi.fn();
      render(
        <Button 
          text="Default" 
          onClick={onClick} 
        />
      );
      
      const button = screen.getByRole('button');
      expect(button).toHaveClass('button-component', 'default');
    });

    it('applies small variation class when small variation provided', () => {
      const onClick = vi.fn();
      render(
        <Button 
          text="Small" 
          onClick={onClick} 
          variation="small" 
        />
      );
      
      const button = screen.getByRole('button');
      expect(button).toHaveClass('button-component', 'small');
    });

    it('has correct button type attribute', () => {
      const onClick = vi.fn();
      render(
        <Button 
          text="Test" 
          onClick={onClick} 
        />
      );
      
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('type', 'button');
    });

    it('handles multiple clicks correctly', () => {
      const onClick = vi.fn();
      render(
        <Button 
          text="Multi Click" 
          onClick={onClick} 
        />
      );
      
      const button = screen.getByRole('button');
      fireEvent.click(button);
      fireEvent.click(button);
      fireEvent.click(button);
      
      expect(onClick).toHaveBeenCalledTimes(3);
    });
  });
});