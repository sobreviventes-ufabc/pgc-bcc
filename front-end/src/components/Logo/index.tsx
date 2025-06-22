import Image from "next/image";

const Logo: React.FC = () => {
    return <Image src="/img/logo.svg" className="app-logo" alt="UFABChat Logo" width={268} height={74} priority />;
};

export default Logo;