
import React, { Fragment } from 'react';
import classNames from 'classnames';
import './Menu.css';

const menuItems = [
  'Home',
  'About',
  'Contact',
];

interface MenuProps {
  isOpen?: boolean;
  onClickBackground?: () => void;
}

const Menu: React.FC<MenuProps> = ({ isOpen = true, onClickBackground }) => {
  return (
    <Fragment>
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
      <div
        className={classNames('menu-bg', { 'open': isOpen })}
        onClick={onClickBackground}
      ></div>
    </Fragment>
  );
};

export default Menu;
