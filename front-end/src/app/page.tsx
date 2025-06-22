import styles from "./page.module.css";
import Logo from "@/components/Logo";
import Input from "@/components/Input";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
      <Logo />
      <Input />
      </main>
      <footer className={styles.footer}>
       
      </footer>
    </div>
  );
}
