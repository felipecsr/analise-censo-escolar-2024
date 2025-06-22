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

   * `raw`: dados brutos originais (ver observação sobre arquivos pesados abaixo).
   * `trusted`: dados tratados, padronizados e com [log de execução](data/2_trusted/microdados_ed_basica_trusted_log.txt) — gerada via Python.
   * `refined`: criada diretamente em SQL no SQLite, com 21 cruzamentos categorizados como "coerente", "inconsistente" ou "inconclusivo" — demonstrando domínio em modelagem analítica declarativa.
3. **Análise exploratória em Jupyter**:

   * Conexão com o banco SQLite.
   * Categorização analítica das flags: diferenciação entre **erros de fato** e **hipóteses investigáveis**.
   * Seleção dos principais cruzamentos de cada grupo.
4. **Camada final para Power BI**:

   * Nova view SQL com os principais cruzamentos selecionados.
   * Power BI conectado diretamente ao SQLite, reforçando integração entre ferramentas e reuso de base local leve.

---

## ⚠️ Sobre os Arquivos de Dados (Boas Práticas)

> **Atenção:**
> Os arquivos completos da camada **raw** e **trusted** ultrapassam 200MB cada.
> Por **boas práticas de versionamento** e para manter o repositório ágil, estes arquivos **NÃO são versionados** diretamente aqui.

* Os arquivos `.csv` completos estão disponíveis para download nos links abaixo.
* O repositório traz apenas **samples** representativos, suficientes para navegação e revisão de pipeline.
* O pipeline está configurado para rodar com os arquivos full — baixe-os conforme instrução.

**Links para os dados completos:**

* **raw:** [Download (Google Drive)](https://drive.google.com/file/d/1UW4RJnRswlulH92xpDo3apPfBG_pBqZt/view?usp=sharing)
* **trusted:** [Download (Google Drive)](https://drive.google.com/file/d/1xRMo-NVvqqJtbARlXSxNHudO9U0CkByw/view?usp=sharing)

**Samples incluídos:**

* `/data/raw/microdados_ed_basica_raw_sample.csv`
* `/data/trusted/microdados_ed_basica_trusted_sample.csv`

---

## 🛠️ Scripts do Pipeline

Scripts principais disponíveis diretamente no repositório:

* [ETL Trusted (Python)](/scripts/etl_trusted.py)
* [ETL Refined (SQL)](/scripts/etl_refined.sql)
* [`refined_top_flags_para_bi.sql`]*(em breve)*

---

## 🧠 Principais Descobertas (em andamento)

* As inconsistências variam em gravidade: algumas indicam erros de fato (ex: ausência de energia em escolas com laboratório); outras, hipóteses legítimas (ex: escola rural com internet).
* A análise exploratória em Python permitiu classificar e priorizar as flags.
* O Power BI apresentará apenas os cruzamentos com maior impacto.

---

## 🛠️ Ferramentas e Metodologias

* **Banco de Dados:** SQLite + DBeaver
* **Linguagens:** SQL, Python (pandas, seaborn, matplotlib, sqlite3)
* **Visualização:** Power BI (conectado diretamente ao SQLite)
* **Zonas de dados:** Estrutura raw → trusted (via Python) → refined (via SQL)
* **Apresentação:** README + Notebook + .pbix + prints + logs

---

## 📂 Estrutura do Repositório

* `/data/raw/`: CSVs originais (completo via link, sample versionado)
* `/data/trusted/`: arquivos tratados (completo via link, sample versionado) + log
* `/data/refined/`: base pronta para análise com 21 cruzamentos de variáveis
* `/scripts/`: scripts ETL (Python e SQL)
* `/notebooks/`: análise exploratória dos 21 cruzamentos e `missing values`, observando seus impactos 
* `/powerbi/`: arquivo .pbix e visuais exportados

---

## 🔭 Em andamento

* Finalizar classificação das 21 flags no notebook.
* Criar view final com principais flags para visualização.
* Publicar dashboards no Power BI com análise visual.
* Incluir prints, GIFs e vídeo explicativo no repositório.

---

## 🛡️ Licença

Este projeto — *Qualidade dos Dados do Censo Escolar (2024)* — é distribuído sob a **GNU General Public License v3.0 (GPLv3)**.
O código, scripts e modelagem estão cobertos por essa licença copyleft, garantindo liberdade de uso, modificação e redistribuição, desde que o mesmo modelo de licença seja mantido.

**Autor:** Felipe Reis (2025)

O conteúdo visual e textual (dashboards, imagens, análises) está licenciado sob **Creative Commons Atribuição 4.0 Internacional (CC-BY 4.0)**.

* 🔗 [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
* 🔗 [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)
