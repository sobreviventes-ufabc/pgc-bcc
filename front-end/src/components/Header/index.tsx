import Image from 'next/image';
import Logo from '@/components/Logo';
import './index.css';

const Header: React.FC = () => {
    return (
        <header className="header-component">
            <div className="header-main-conent">
                <div className="header-menu">
                    <button
                      type="button"
                      className="header-menu-button">
                        <Image
                          src="/img/icon-burger.svg"
                          className="header-icon-menu"
                          alt="Menu"
                          width={36}
                          height={24} />
                    </button>
                </div>

                <div className="header-logo">
                    <Logo size="small" />
                </div>

                <div className="header-new-chat">
                    <button
                      type="button"
                      className="header-new-chat-button">
                        <Image
                          src="/img/icon-new-chat.svg"
                          className="header-icon-menu"
                          alt="Menu"
                          width={47}
                          height={47} />
                    </button>
                </div>
            </div>
            <div className="header-line"></div>
        </header>
    );
};

export default Header;