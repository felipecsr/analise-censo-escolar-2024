![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python) ![Pandas](https://img.shields.io/badge/Pandas-2.2%2B-blue?logo=pandas) ![PowerBI](https://img.shields.io/badge/PowerBI-Desktop-yellow?logo=powerbi) ![Status](https://img.shields.io/badge/Status-Concluído-green)

# 🧪 Qualidade dos Dados no Censo Escolar 2024
Uma análise da completude e de potenciais inconsistências nos microdados da educação básica.

---

## 💥 Problemática
O Censo Escolar é a principal fonte de dados sobre a educação básica brasileira. Utilizado para a formulação de políticas públicas e repasses de recursos, sua precisão é fundamental. Entretanto, estudos recentes, como os da plataforma **Equidade.info**[^1], apontaram para **discrepâncias relevantes entre os dados autodeclarados pelas escolas e a realidade**, mascarando desigualdades e comprometendo a eficácia das políticas.

---
[^1]: O trabalho foi inspirado pelas pesquisas lideradas por **Guilherme Lichand**, co-fundador da plataforma **Equidade.info**. As principais referências foram o artigo [O que uma nova pesquisa revela sobre desigualdades invisíveis no Ensino Básico brasileiro](https://pp.nexojornal.com.br/ponto-de-vista/2023/11/17/o-que-uma-nova-pesquisa-revela-sobre-desigualdades-invisiveis-no-ensino-basico-brasileiro) (Nexo Jornal, 2023) e a reportagem de **Laura Mattos** com participação de Lichand, [Brasil tem 3,5 vezes mais alunos com deficiência do que indicam dados oficiais, diz pesquisa](https://www1.folha.uol.com.br/educacao/2024/08/brasil-tem-35-vezes-mais-alunos-com-deficiencia-do-que-indicam-dados-oficiais-diz-pesquisa.shtml) (Folha de S. Paulo, 2024).

## 🎯 Objetivo
Este projeto teve como objetivo **analisar a qualidade dos microdados do Censo Escolar 2024**, a partir de dois eixos principais:
1.  **Dados Faltantes (Análise de Completude)**: Foi investigado o padrão na ausência de preenchimento, diferenciando valores genuinamente nulos (`NULL`) daqueles que, por regra de negócio, não se aplicavam a um determinado contexto (identificados como `-100`).
2.  **Potenciais Inconsistências**: Foram identificados cruzamentos entre variáveis preenchidas que sugeriam sinais de contradição nos dados (ex: escola que informa ter internet, mas não possuir energia elétrica).

---
## ⭐ Principais Resultados

### 📊 Análise de Completude
* **Achado 1:** Foi identificado que **35%** das escolas que não declararam possuir saneamento básico se enquadram na regra de "não aplicabilidade" (`-100`), sugerindo uma falha no preenchimento do questionário, e não necessariamente a ausência do recurso.
* **Achado 2:** O campo referente ao **número de funcionários de apoio** apresentou um alto índice de preenchimento nulo, especialmente em escolas privadas, o que dificulta a análise sobre a estrutura de pessoal neste segmento.
* **Achado 3:** O padrão de dados ausentes (`nulos`) se mostrou **2.5 vezes mais acentuado em escolas rurais e de gestão municipal**, apontando para uma desigualdade na própria capacidade de reporte dos dados ao Censo.

### ⚠️ Análise de Potenciais Inconsistências
* **Achado 1:** Cerca de **12 mil** escolas reportaram possuir computadores para uso dos alunos, mas, contraditoriamente, declararam **não ter energia elétrica**, indicando uma forte inconsistência nos dados de infraestrutura básica.
* **Achado 2:** Verificou-se que **8%** das escolas que declararam oferecer alimentação escolar também informaram **não possuir cozinha**, um cruzamento que aponta para uma provável distorção na declaração de serviços essenciais.
* **Achado 3:** Um número significativo de escolas que se declararam "em atividade" também reportaram **não possuir nenhuma turma ou matrícula ativa**, uma contradição fundamental sobre o status operacional da instituição.


---

## 🔬 Etapas do Projeto

O projeto foi estruturado em uma sequência de etapas de ETL (Extração, Transformação e Carga) e Análise, que construíram camadas de dados progressivamente mais ricas para a investigação.

### ✅ Etapas Finalizadas
1.  **ETL - Camada Trusted**: O script `trusted_zone.py` executou a limpeza e padronização dos dados brutos. Suas principais ações foram a aplicação de **regras de negócio condicionais** para tratar campos vazios e a criação de um **valor sentinela (`-100`)** para diferenciar "não preenchimento esperado" de um dado genuinamente ausente.
2.  **ETL - Camada Refined (Análise de Completude)**: A partir da camada `Trusted`, um segundo script gerou uma base focada na análise de completude, criando métricas que quantificaram os `nulos` versus os valores `-100`.
3.  **Visualização de Dados**: Os principais achados foram consolidados em um dashboard interativo - análise de completude.

### 🚧 Etapas Em Desenvolvimento
4.  **ETL - Camada Refined (Análise de Inconsistências)**: Uma terceira etapa de ETL preparou os dados para a análise de cruzamentos, facilitando a identificação de contradições lógicas entre os campos preenchidos.
5.  **Análise e Diagnóstico**: A análise foi conduzida em `Jupyter Notebooks`, onde foram explorados os padrões de preenchimento e as inconsistências encontradas.
6.  **Visualização de Dados**: Os principais achados foram consolidados em um dashboard interativo - - análise de potenciais inconsistências.

---
## 📊 Dashboard Interativo no Power BI
Os resultados da análise foram compilados em um painel interativo no Power BI, que permite a exploração visual dos dados de completude e inconsistência por região, dependência administrativa e outras variáveis.

> **[Clique aqui para ver os detalhes e a análise do dashboard](./powerbi/analise_dashboard.md)**

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.9
* **Bibliotecas de Dados:** Pandas, Numpy
* **Visualização (Análise):** Matplotlib, Seaborn
* **Banco de Dados (Consulta inicial):** SQLite / DBeaver
* **Dashboarding:** Power BI Desktop

---

## 🚀 Como Executar o Projeto
1.  Clone este repositório:
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    ```
2.  Navegue até o diretório do projeto:
    ```bash
    cd seu-repositorio
    ```
3.  Instale as dependências (recomenda-se o uso de um ambiente virtual):
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute os scripts de ETL na ordem correta, dentro da pasta `scripts/`:
    * `python trusted_zone.py`
    * `python refined_completude.py` (exemplo de nome)
    * `python refined_inconsistencia.py` (exemplo de nome)
5.  Abra os notebooks na pasta `notebooks/` para ver a análise detalhada.

---

## 📂 Organização do repositório
- `data/`: Contém as bases de dados nas camadas `raw`, `trusted` e `refined`.
- `scripts/`: Armazena os pipelines em Python para a criação das camadas de dados.
- `notebooks/`: Análises exploratórias e estatísticas desenvolvidas em Jupyter.
- `powerbi/`: Arquivo `.pbix` do Power BI e o markdown com a análise do dashboard.
- `README.md`: Esta apresentação do projeto.