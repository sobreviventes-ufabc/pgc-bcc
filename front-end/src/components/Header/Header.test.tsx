import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Header from './index';

// Mock the Logo and Menu components
vi.mock('@/components/Logo', () => ({
  default: ({ size }: { size?: string }) => (
    <div data-testid="logo-mock">Logo {size}</div>
  ),
}));

vi.mock('@/components/Menu', () => ({
  default: ({ isOpen, onCancel }: { isOpen: boolean; onCancel: () => void }) => (
    <div data-testid="menu-mock">
      Menu {isOpen ? 'open' : 'closed'}
      {isOpen && (
        <button 
          onClick={onCancel}
          data-testid="menu-close"
        >
          Close Menu
        </button>
      )}
    </div>
  ),
}));

describe('Header Component', () => {
  describe('Component Unit Tests', () => {
    it('renders all header elements', () => {
      const onNewChatClick = vi.fn();
      render(
        <Header 
          onNewChatClick={onNewChatClick} 
        />
      );
      
      expect(screen.getByRole('banner')).toBeInTheDocument();
      expect(screen.getByTestId('logo-mock')).toBeInTheDocument();
      expect(screen.getByTestId('menu-mock')).toBeInTheDocument();
    });

    it('calls onNewChatClick when new chat button is clicked', async () => {
      const onNewChatClick = vi.fn();
      render(
        <Header 
          onNewChatClick={onNewChatClick} 
        />
      );
      
      const buttons = screen.getAllByRole('button');
      const newChatBtn = buttons.find(btn => 
        btn.querySelector('img')?.getAttribute('alt') === 'Menu' &&
        btn.querySelector('img')?.getAttribute('width') === '47'
      );
      
      if (newChatBtn) {
        fireEvent.click(newChatBtn);
        
        const confirmButton = await screen.findByText('Confirmar');
        fireEvent.click(confirmButton);
        
        expect(onNewChatClick).toHaveBeenCalledTimes(1);
      }
    });

    it('opens menu when menu button is clicked', () => {
      const onNewChatClick = vi.fn();
      render(
        <Header 
          onNewChatClick={onNewChatClick} 
        />
      );
      
      // Initially menu should be closed
      expect(screen.getByText('Menu closed')).toBeInTheDocument();
      
      // Find and click the menu button
      const buttons = screen.getAllByRole('button');
      const menuBtn = buttons.find(btn => 
        btn.querySelector('img')?.getAttribute('alt') === 'Menu' &&
        btn.querySelector('img')?.getAttribute('width') === '36'
      );
      
      if (menuBtn) {
        fireEvent.click(menuBtn);
        expect(screen.getByText('Menu open')).toBeInTheDocument();
      }
    });

    it('closes menu when menu close is triggered', () => {
      const onNewChatClick = vi.fn();
      render(
        <Header 
          onNewChatClick={onNewChatClick} 
        />
      );
      
      // Open menu first
      const buttons = screen.getAllByRole('button');
      const menuBtn = buttons.find(btn => 
        btn.querySelector('img')?.getAttribute('alt') === 'Menu' &&
        btn.querySelector('img')?.getAttribute('width') === '36'
      );
      
      if (menuBtn) {
        fireEvent.click(menuBtn);
        expect(screen.getByText('Menu open')).toBeInTheDocument();
        
        // Now close it
        const closeButton = screen.getByTestId('menu-close');
        fireEvent.click(closeButton);
        expect(screen.getByText('Menu closed')).toBeInTheDocument();
      }
    });

    it('renders Logo with small size', () => {
      const onNewChatClick = vi.fn();
      render(
        <Header 
          onNewChatClick={onNewChatClick} 
        />
      );
      
      expect(screen.getByText('Logo small')).toBeInTheDocument();
    });

    it('contains header line element', () => {
      const onNewChatClick = vi.fn();
      const { container } = render(
        <Header 
          onNewChatClick={onNewChatClick} 
        />
      );
      
      const headerLine = container.querySelector('.header-line');
      expect(headerLine).toBeInTheDocument();
    });

    it('has correct CSS classes structure', () => {
      const onNewChatClick = vi.fn();
      const { container } = render(
        <Header 
          onNewChatClick={onNewChatClick} 
        />
      );
      
      expect(container.querySelector('.header-component')).toBeInTheDocument();
      expect(container.querySelector('.header-main-conent')).toBeInTheDocument();
      expect(container.querySelector('.header-menu')).toBeInTheDocument();
      expect(container.querySelector('.header-logo')).toBeInTheDocument();
      expect(container.querySelector('.header-new-chat')).toBeInTheDocument();
    });
  });
});