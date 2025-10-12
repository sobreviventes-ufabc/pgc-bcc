import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Menu from './index';

describe('Menu Component', () => {
  describe('Component Unit Tests', () => {
    it('renders menu when isOpen is true', () => {
      render(
        <Menu 
          isOpen={true} 
        />
      );
      
      expect(screen.getByRole('navigation')).toBeInTheDocument();
      expect(screen.getByText('Menu')).toBeInTheDocument();
    });

    it('renders background overlay when isOpen is true', () => {
      const { container } = render(
        <Menu 
          isOpen={true} 
        />
      );
      
      const overlay = container.querySelector('.menu-bg');
      expect(overlay).toBeInTheDocument();
      expect(overlay).toHaveClass('open');
    });

    it('does not render background overlay when isOpen is false', () => {
      const { container } = render(
        <Menu 
          isOpen={false} 
        />
      );
      
      const overlay = container.querySelector('.menu-bg');
      expect(overlay).not.toBeInTheDocument();
    });

    it('applies menu-open class when isOpen is true', () => {
      const { container } = render(
        <Menu 
          isOpen={true} 
        />
      );
      
      const menuNav = container.querySelector('.menu-component');
      expect(menuNav).toHaveClass('menu-open');
    });

    it('does not apply menu-open class when isOpen is false', () => {
      const { container } = render(
        <Menu 
          isOpen={false} 
        />
      );
      
      const menuNav = container.querySelector('.menu-component');
      expect(menuNav).not.toHaveClass('menu-open');
    });

    it('renders all menu items', () => {
      render(
        <Menu 
          isOpen={true} 
        />
      );
      
      expect(screen.getByText('Novo chat')).toBeInTheDocument();
      expect(screen.getByText('Sobre')).toBeInTheDocument();
    });

    it('renders menu items with correct links', () => {
      render(
        <Menu 
          isOpen={true} 
        />
      );
      
      const novoChatLink = screen.getByRole('link', { name: 'Novo chat' });
      const sobreLink = screen.getByRole('link', { name: 'Sobre' });
      
      expect(novoChatLink).toHaveAttribute('href', '/');
      expect(sobreLink).toHaveAttribute('href', '/about');
    });

    it('calls onCancel when background overlay is clicked', () => {
      const onCancel = vi.fn();
      const { container } = render(
        <Menu 
          isOpen={true} 
          onCancel={onCancel} 
        />
      );
      
      const overlay = container.querySelector('.menu-bg');
      if (overlay) {
        fireEvent.click(overlay);
        expect(onCancel).toHaveBeenCalledTimes(1);
      }
    });

    it('does not call onCancel when menu content is clicked', () => {
      const onCancel = vi.fn();
      render(
        <Menu 
          isOpen={true} 
          onCancel={onCancel} 
        />
      );
      
      const menuTitle = screen.getByText('Menu');
      fireEvent.click(menuTitle);
      
      expect(onCancel).not.toHaveBeenCalled();
    });

    it('defaults to isOpen true when no prop provided', () => {
      const { container } = render(<Menu />);
      
      const menuNav = container.querySelector('.menu-component');
      expect(menuNav).toHaveClass('menu-open');
    });

    it('renders menu items with correct CSS classes', () => {
      const { container } = render(
        <Menu 
          isOpen={true} 
        />
      );
      
      const menuItems = container.querySelectorAll('.menu-item');
      const menuLinks = container.querySelectorAll('.menu-link');
      
      expect(menuItems).toHaveLength(2);
      expect(menuLinks).toHaveLength(2);
    });

    it('renders menu title with correct heading level', () => {
      render(
        <Menu 
          isOpen={true} 
        />
      );
      
      const menuTitle = screen.getByRole('heading', { level: 3 });
      expect(menuTitle).toHaveTextContent('Menu');
    });

    it('renders as navigation landmark', () => {
      render(
        <Menu 
          isOpen={true} 
        />
      );
      
      const nav = screen.getByRole('navigation');
      expect(nav).toHaveClass('menu-component');
    });
  });
});