import classNames from 'classnames';
import './index.css';


interface ChatTextProps {
    children: React.ReactNode;
    variation: 'sent' | 'received' | 'loading';
}

const ChatText: React.FC<ChatTextProps> = ({ children, variation }) => {
    return (
        <div className={classNames('chat-text-component', '--' + variation)}>
            <div className="chat-text-container">
                {children}
            </div>
        </div>
    );
};

export default ChatText;