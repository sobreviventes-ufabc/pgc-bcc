'use client';

import GreenBackground from '@/components/GreenBackground';
import Logo from '@/components/Logo';
import { useRouter } from 'next/navigation';
import Button from '@/components/Button';

import './page.css';

export default function AboutPage() {
  const router = useRouter();
  return (
    <GreenBackground>
      <div className="about-container">
        <div className="about-logo">
          <Logo />
        </div>
        <div className="about-content">
          <p>
            {'O assistente virtual desenvolvido tem como propósito facilitar o acesso dos estudantes da UFABC a informações acadêmicas essenciais. Ele utiliza técnicas avançadas de Inteligência Artificial, especialmente a abordagem de Geração Aumentada por Recuperação (RAG), que permite buscar dados em documentos institucionais e gerar respostas precisas, atualizadas e confiáveis.'}
          </p>
          <p>
            {'A ferramenta reúne em um só lugar informações que hoje estão espalhadas em sites, regulamentos e editais, respondendo dúvidas sobre matrícula, oferta de disciplinas, normas acadêmicas e aspectos administrativos. Dessa forma, ajuda a reduzir a fragmentação dos canais de comunicação, tornando o processo de tomada de decisão mais ágil e seguro para os discentes.'}
          </p>
          <p>
            {'Este é um Projeto de Graduação em Computação (PGC), desenvolvido por Aline M. M. dos Santos, Leonardo P. de Oliveira e Matheus V. de Araujo, com orientação do Prof. Dr. Francisco Javier Ropero Peláez.'}
          </p>
        </div>
        <Button
          text="Voltar"
          onClick={() => router.back()}
        />
      </div>
    </GreenBackground>
  );
}
