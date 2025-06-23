import classNames from 'classnames';
import './index.css';

interface ChatTextProps {
    text: string
    variation: "sent" | "received"
}

const ChatText: React.FC<ChatTextProps> = ({ text, variation }) => {
    return (
        <div className={classNames("chat-text-component", "--"+variation)}>
            <div className="chat-text-container">
                {text}
            </div>
        </div>
    )
};

export default ChatText;