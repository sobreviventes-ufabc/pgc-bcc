import json
import uuid
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .retry import retry_with_backoff
from ..core.models import get_llama_model

def reestruturar_tabelas(html_limpo: str) -> str:
    """
    Normaliza uma única tabela HTML, aplicando regras de calendário e limpeza.
    """
    prompt_template = """
Você é um normalizador de tabelas extraídas de PDFs institucionais.

Entrada: um ou mais blocos de <table> em HTML, extraídos de diferentes tipos de documentos 
(ex: calendário acadêmico, horários de ônibus, escalas de sala, listas de presença etc.).

Esses blocos podem ter problemas como:
- Cabeçalhos faltando ou quebrados
- Meses ausentes ou colados (em tabelas de calendário)
- Datas grudadas (ex: "De09a23" → "De 09 a 23")
- Colunas duplicadas com sufixos como ".1"
- Linhas vazias ou só com NaN/valores inválidos
- Caracteres estranhos como "|", "—", "="

Sua tarefa é:

1. **Detectar o tipo de tabela.**
   - Se for **calendário acadêmico** (meses, prazos, colação de grau, matrícula, lançamento de conceitos, avaliações etc.):
     - Garantir que **cada mês** (Janeiro, Fevereiro, Março, …) esteja em uma tabela separada.
     - Se o mês não tiver cabeçalho explícito, deduza pelo contexto (ex: aparece logo após Janeiro e antes de Março → é Fevereiro).
     - Criar `<thead><tr><th colspan="2">NOME_DO_MÊS[/ANO]</th></tr></thead>` para identificar o mês.
     - Regra prática: "Solicitação de Colação de Grau de X" → pertence ao mês anterior e deve ser o **último item dessa tabela**. Ex.: "Solicitação de Colação de Grau de Março" → último item de Fevereiro.
   - **Se não for calendário acadêmico** (ex: escala de trabalho, horários de ônibus, listas de nomes, etc.):
     - **Não invente meses** nem cabeçalhos artificiais.
     - **Nunca use "INDEFINIDO"**. Apenas corrija a estrutura e mantenha o conteúdo original.

2. **Corrigir formatação geral em qualquer tabela:**
   - Inserir espaços faltantes em datas (`De09a23` → `De 09 a 23`).
   - Remover símbolos estranhos como `|`, `—`, `=`.
   - Ajustar cabeçalhos de colunas duplicadas (remover `.1`).
   - Excluir linhas vazias ou só com NaN.
   - Garantir que seja HTML válido.

3. **Restrições:**
   - Nunca inventar dados novos.
   - Nunca agrupar meses diferentes em uma mesma tabela.
   - Sempre retornar **cada <table> em linha única**, sem quebras de linha, espaços extras ou comentários.

---

### Exemplos

Exemplo de entrada (calendário acadêmico):
<table><thead><tr><th colspan="2">JANEIRO</th></tr></thead><tbody><tr><td>De 06/01 a 07/02</td><td>Lançamento de conceitos de 2024.3</td></tr><tr><td>De09a23</td><td>Avaliação de Disciplinas 3º quadrimestre 2024</td></tr><tr><td>30 (12h) a 31 (23h59) |</td><td>Ajuste de Matrículas em Disciplinas - 1º quadrimestre de 2025</td></tr><tr><td>De01a31</td><td>Solicitação de Colação de Grau de Fevereiro — exclusivo para concluintes até 2024.2**</td></tr><tr><td>31</td><td>Colação de Grau — exclusivo para concluintes até o 2º quadrimestre de 2024</td></tr></tbody></table> <table><thead><tr><th>01</th><th>Conclusão do 3º quadrimestre de 2024</th></tr></thead><tbody><tr><td>De 03a 05</td><td>Solicitação excepcional de matrícula em disciplina - 1º quadrimestre de 2025</td></tr><tr><td>De 04 a 10</td><td>Solicitação do regime de guarda religiosa- 1º quadrimestre de 2025</td></tr><tr><td>De 03a 04</td><td>Solicitação de Matrícula — Aluno Especial - 1º quadrimestre de 2025</td></tr><tr><td>De 10 a 24</td><td>Avaliação de Disciplinas 3º quadrimestre 2024</td></tr><tr><td>10</td><td>Início das Aulas - 1º quadrimestre (veteranos)</td></tr><tr><td>De 104 14</td><td>Solicitação de matrícula em Trabalho de Graduação das Engenharias, Trabalho de Conclusão de Curso de BRI/BPP/BPT e Monografia do BCE</td></tr><tr><td>De 10 a 18</td><td>Solicitação de Revisão de Conceito e de Instrumentos Avaliativos (ref. 2024.3)</td></tr><tr><td>De 10 a 16</td><td>Solicitação de Cancelamento de Disciplinas</td></tr><tr><td>De17a21</td><td>Solicitação de Aproveitamento de Disciplina como Livre Escolha</td></tr><tr><td>De17a21</td><td>Solicitação de Equivalência de Disciplina</td></tr><tr><td>18 (12h) a 19 (23h59) |</td><td>Reajuste de Matrículas em Disciplinas - 1º quadrimestre de 2025</td></tr><tr><td>28</td><td>Colação de Grau — exclusivo para concluintes até o 2º quadrimestre de 2024</td></tr></tbody></table>

Exemplo de saída:
<table><thead><tr><th colspan="2">JANEIRO</th></tr></thead><tbody><tr><td>De 06/01 a 07/02</td><td>Lançamento de conceitos de 2024.3</td></tr><tr><td>De 09 a 23</td><td>Avaliação de Disciplinas 3º quadrimestre 2024</td></tr><tr><td>30 (12h) a 31 (23h59)</td><td>Ajuste de Matrículas em Disciplinas - 1º quadrimestre de 2025</td></tr><tr><td>De 01 a 31</td><td>Solicitação de Colação de Grau de Fevereiro — exclusivo para concluintes até 2024.2**</td></tr><tr><td>31</td><td>Colação de Grau — exclusivo para concluintes até o 2º quadrimestre de 2024</td></tr></tbody></table><table><thead><tr><th colspan="2">FEVEREIRO</th></tr></thead><tbody><tr><td>De 03 a 05</td><td>Solicitação excepcional de matrícula em disciplina - 1º quadrimestre de 2025</td></tr><tr><td>De 04 a 10</td><td>Solicitação do regime de guarda religiosa- 1º quadrimestre de 2025</td></tr><tr><td>De 03 a 04</td><td>Solicitação de Matrícula — Aluno Especial - 1º quadrimestre de 2025</td></tr><tr><td>De 10 a 24</td><td>Avaliação de Disciplinas 3º quadrimestre 2024</td></tr><tr><td>10</td><td>Início das Aulas - 1º quadrimestre (veteranos)</td></tr><tr><td>De 10 a 14</td><td>Solicitação de matrícula em Trabalho de Graduação das Engenharias, Trabalho de Conclusão de Curso de BRI/BPP/BPT e Monografia do BCE</td></tr><tr><td>De 10 a 18</td><td>Solicitação de Revisão de Conceito e de Instrumentos Avaliativos (ref. 2024.3)</td></tr><tr><td>De 10 a 16</td><td>Solicitação de Cancelamento de Disciplinas</td></tr><tr><td>De 17 a 21</td><td>Solicitação de Aproveitamento de Disciplina como Livre Escolha</td></tr><tr><td>De 17 a 21</td><td>Solicitação de Equivalência de Disciplina</td></tr><tr><td>18 (12h) a 19 (23h59)</td><td>Reajuste de Matrículas em Disciplinas - 1º quadrimestre de 2025</td></tr><tr><td>28</td><td>Colação de Grau — exclusivo para concluintes até o 2º quadrimestre de 2024</td></tr></tbody></table>

---

Exemplo de entrada (não calendário — horários de ônibus):
<table><thead><tr><th>Linha</th><th>Partida</th><th>Chegada</th></tr></thead><tbody><tr><td>1</td><td>06:50</td><td>07:25</td></tr></tbody></table>

Exemplo de saída (não criar meses):
<table><thead><tr><th>Linha</th><th>Partida</th><th>Chegada</th></tr></thead><tbody><tr><td>1</td><td>06:50</td><td>07:25</td></tr></tbody></table>

---

**Importante:**  
A resposta deve conter **apenas as tabelas corrigidas**, sem explicações.  
A saída deve iniciar com `<table>` e terminar com `</table>`, podendo haver múltiplas tabelas.  
Cada tabela deve estar em **linha única**, sem quebras de linha nem comentários.

Tabela a corrigir:
{html_limpo}
"""
    model = get_llama_model()
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | model | StrOutputParser()

    return retry_with_backoff(lambda: chain.invoke({"html_limpo": html_limpo}))