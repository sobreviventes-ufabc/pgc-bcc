
import React from 'react';
import classNames from 'classnames';
import './Menu.css';

const menuItems = [
  'Home',
  'About',
  'Contact',
];

interface MenuProps {
  isOpen?: boolean;
}

const Menu: React.FC<MenuProps> = ({ isOpen = true }) => {
  return (
    <nav className={classNames('menu-component', { 'menu-open': isOpen })}>
      <div className="menu-title">
          <h3>Menu</h3>
      </div>
      <ul>
        {menuItems.map((item, idx) => (
          <li
            key={item + idx}
            className="menu-item">
            <a href={`/${item.toLowerCase()}`}>{item}</a>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Menu;
