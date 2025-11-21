
import React, { Fragment } from 'react';
import classNames from 'classnames';
import './Menu.css';

const menuItems = [
  {
    title: 'Novo chat',
    link: '/'
  },
  {
    title: 'Sobre',
    link: '/about'
  }
];

interface MenuProps {
  isOpen?: boolean;
  onCancel?: () => void;
  onNewChatClick?: () => void;
}

const Menu: React.FC<MenuProps> = ({ isOpen = true, onCancel, onNewChatClick }) => {
  const handleItemClick = (e: React.MouseEvent, item: typeof menuItems[0]) => {
    if (item.title === 'Novo chat' && onNewChatClick) {
      e.preventDefault();
      onNewChatClick();
      if (onCancel) onCancel();
    }
  };

  return (
    <Fragment>
      {isOpen && (
        <div
          className={classNames('menu-bg', { 'open': isOpen })}
          onClick={onCancel}
        ></div>
      )}
      <nav className={classNames('menu-component', { 'menu-open': isOpen })}>
        <div className="menu-title">
            <h3>Menu</h3>
        </div>
        <ul>
          {menuItems.map((item, idx) => (
            <li
              key={idx}
              className="menu-item">
              <a
                className="menu-link"
                href={item.link}
                onClick={(e) => handleItemClick(e, item)}
              >
                {item.title}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </Fragment>
  );
};

export default Menu;
