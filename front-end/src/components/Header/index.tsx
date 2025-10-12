'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import Logo from '@/components/Logo';
import Menu from '@/components/Menu';
import './index.css';

interface HeaderProps {
    onNewChatClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onNewChatClick }) => {
    const [menuOpen, setMenuOpen] = useState(false);

    const handleMenuClick = () => setMenuOpen(true);
    const handleMenuClose = () => setMenuOpen(false);

    return (
        <header className="header-component">
            <div className="header-main-conent container">
                <div className="header-menu">
                    <button
                      type="button"
                      className="header-menu-button"
                      onClick={handleMenuClick}
                    >
                        <Image
                          src="/img/icon-burger.svg"
                          className="header-icon-menu"
                          alt="Menu"
                          width={36}
                          height={24}
                        />
                    </button>
                </div>

                <div className="header-logo">
                    <Logo size="small" />
                </div>

                <div className="header-new-chat">
                    <button
                      type="button"
                      className="header-new-chat-button"
                      onClick={onNewChatClick}
                    >
                        <Image
                          src="/img/icon-new-chat.svg"
                          className="header-icon-menu"
                          alt="Menu"
                          width={47}
                          height={47}
                        />
                    </button>
                </div>
            </div>
            <div className="header-line"></div>
            <Menu
              isOpen={menuOpen}
              onCancel={handleMenuClose}
            />
        </header>
    );
};

export default Header;