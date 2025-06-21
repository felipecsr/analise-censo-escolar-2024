# Qualidade dos Dados no Censo Escolar (2024)

## 📌 Contexto e Motivação

O Censo Escolar é a principal base de dados educacional do país e subsidia políticas públicas, repasse de verbas e diagnósticos sobre a educação básica. No entanto, a qualidade das respostas autodeclaradas por escolas pode comprometer a confiabilidade dessas decisões.

Este projeto investiga inconsistências nos dados do Censo Escolar de 2024, propondo formas de identificá-las e refletindo sobre seus impactos nas políticas educacionais.

---

## 🎯 Objetivo

Detectar e analisar falhas de preenchimento nas variáveis autodeclaradas do Censo Escolar, observando como elas se distribuem por região, tipo de rede (municipal, estadual, privada) e características das escolas.

---

## 🔄 Pipeline do Projeto

1. **Exploração inicial**: leitura do dicionário de dados e observações iniciais sobre o CSV.
2. **Construção das camadas de dados**:
   - `raw`: dados brutos originais (ver observação sobre arquivos pesados abaixo).
   - `trusted`: dados tratados, padronizados e com logs detalhados de execução.
   - `refined`: estrutura final enriquecida com flags de inconsistências e logs de execução.
3. **Validações e primeiros resultados**:
   - **Trusted** já pronta e validada, garantindo consistência dos dados-base.
   - **Refined** criada com flags de inconsistência para diagnósticos críticos.
4. **Próximas etapas (em andamento)**:
   - **Análise de nulos e padrões de preenchimento** (Jupyter Notebook): breve investigação exploratória dos campos críticos na camada trusted.
   - **Visualizações e análise das flags** (Power BI): dashboards interativos mostrando distribuição das inconsistências por rede, região, tipo de escola, além de rankings e destaques visuais.
   - Prints, GIFs e/ou vídeo explicativo serão incluídos ao final do processo.

---

## ⚠️ Sobre os Arquivos de Dados (Boas Práticas)

> **Atenção:**  
> Os arquivos completos da camada **raw** e **trusted** ultrapassam 200MB cada.  
> Por **boas práticas de versionamento** e para manter o repositório ágil, estes arquivos **NÃO são versionados** diretamente aqui.  
>  
> - Os arquivos `.csv` completos estão disponíveis para download nos links abaixo.  
> - O repositório traz apenas **samples** representativos, suficientes para navegação e revisão de pipeline.
> - O pipeline está configurado para rodar com os arquivos full — baixe-os conforme instrução.

**Links para os dados completos:**
- **raw:** [Download (Google Drive)](https://drive.google.com/file/d/1UW4RJnRswlulH92xpDo3apPfBG_pBqZt/view?usp=sharing)
- **trusted:** [Download (Google Drive)](https://drive.google.com/file/d/1xRMo-NVvqqJtbARlXSxNHudO9U0CkByw/view?usp=sharing)

**Samples incluídos:**
- `/data/raw/microdados_ed_basica_raw_sample.csv`
- `/data/trusted/microdados_ed_basica_trusted_sample.csv`

---

## 📑 Logs de Execução

Para reforçar transparência, organização e monitoramento de escalabilidade, os logs de execução das principais etapas estão disponíveis:

- [Log do ETL trusted](data/2_trusted/microdados_ed_basica_trusted_log.txt)
- [Log do ETL refined](data/3_refined/microdados_ed_basica_refined_log.txt)

Os logs incluem informações como início/fim da execução, quantidade de linhas processadas, padronizações aplicadas, tempo total, e eventuais mensagens relevantes.

---

## 🛠️ Scripts do Pipeline

Scripts principais disponíveis diretamente no repositório:

- [ETL Trusted (`etl_trusted.py`)](data/2_trusted/etl_trusted.py)
- [ETL Refined (`etl_refined.py`)](data/3_refined/etl_refined.py)

---

## 🧠 Principais Descobertas (provisórias)

- [Exemplo] Cerca de 12% das escolas que declararam ter laboratório não possuem energia elétrica.
- [Exemplo] As inconsistências concentram-se principalmente em redes municipais da região Norte.

*Os dados acima são placeholders e serão atualizados conforme avançam as análises.*

---

## 🛠️ Ferramentas e Metodologias

- **Banco de Dados:** SQLite + DBeaver
- **Linguagens:** SQL, Python (pandas, seaborn)
- **Visualização:** Power BI
- **Organização:** Estrutura raw → trusted → refined
- **Apresentação:** README + GIFs + vídeo (opcional)

---

## 📂 Estrutura do Repositório

- `/data/raw/`: CSVs originais (completo via link, sample versionado)
- `/data/trusted/`: arquivos tratados (completo via link, sample versionado) + log
- `/data/refined/`: base final enriquecida com flags + log
- `/scripts/`: scripts ETL
- `/notebooks/`: scripts exploratórios e análises em Python
- `/powerbi/`: arquivos .pbix e prints dos dashboards

---

## 🔭 Próximos Passos

- Explorar padrões de ausência de dados e anomalias relevantes na trusted via Jupyter Notebook.
- Publicar dashboards no Power BI com análise visual das flags.
- Incluir imagens, GIFs e vídeo explicativo no repositório.

*Essas etapas estão em desenvolvimento e serão atualizadas em breve.*

---

## 🛡️ Licença

Este projeto — *Qualidade dos Dados do Censo Escolar (2024)* — é distribuído sob a **GNU General Public License v3.0 (GPLv3)**.  
O código, scripts e modelagem estão cobertos por essa licença copyleft, garantindo liberdade de uso, modificação e redistribuição, desde que o mesmo modelo de licença seja mantido.

**Autor:** Felipe Reis (2025)

O conteúdo visual e textual (dashboards, imagens, análises) está licenciado sob **Creative Commons Atribuição 4.0 Internacional (CC-BY 4.0)**.

- 🔗 [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
- 🔗 [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)
