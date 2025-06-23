import Image from 'next/image';

interface LogoProps {
    size?: 'default' | 'small';
}

const Logo: React.FC<LogoProps> = ({ size = 'default' }) => {
    const dimensions = size === 'small' ? { width: 146, height: 38 } : { width: 268, height: 74 };

    return <Image
      src="/img/logo.svg"
      className="app-logo"
      alt="UFABChat Logo"
      width={dimensions.width}
      height={dimensions.height}
      priority />;
};

export default Logo;