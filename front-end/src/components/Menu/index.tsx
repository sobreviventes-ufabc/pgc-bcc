
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
  onClickBackground?: () => void;
}

const Menu: React.FC<MenuProps> = ({ isOpen = true, onClickBackground }) => {
  return (
    <Fragment>
      {isOpen && (
        <div
          className={classNames('menu-bg', { 'open': isOpen })}
          onClick={onClickBackground}
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
