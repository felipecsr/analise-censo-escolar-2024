![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python) ![Pandas](https://img.shields.io/badge/Pandas-2.2%2B-blue?logo=pandas) ![PyArrow](https://img.shields.io/badge/PyArrow-blue?logo=apache) ![PowerBI](https://img.shields.io/badge/PowerBI-Desktop-yellow?logo=powerbi) ![Status](https://img.shields.io/badge/Status-Em_andamento-yellow)

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
* **Achado 1:** O fator mais determinante para a ausência de dados é a localização da escola: zonas rurais apresentam uma taxa de não preenchimento de 23%, mais que o dobro da encontrada em zonas urbanas (9%). Essa disparidade é ainda mais acentuada em regiões como o Sudeste (41% rural vs. 11% urbano).
* **Achado 2:** Existe uma grande variação geográfica e administrativa na qualidade dos dados. Estados como Minas Gerais (29% de nulos) contrastam fortemente com o Paraná (4,5%). Nacionalmente, escolas de gestão privada (16%) e municipal (14%) possuem taxas de nulos significativamente maiores que as estaduais (10%) e federais (2,3%).
* **Achado 3:** A concentração de dados faltantes em estratos específicos (rural, certos estados e dependências) aponta para uma fragilidade sistêmica no método de coleta. A conclusão é que o processo, por ser rígido e uniforme, falha em se adaptar e reforçar o preenchimento em contextos sabidamente mais desafiadores.

### ⚠️ Análise de Potenciais Inconsistências

*Em desenvolvimento*


---

## 🔬 Etapas do Projeto

O projeto foi estruturado em uma sequência de etapas de ETL (Extração, Transformação e Carga) e Análise, que construíram camadas de dados progressivamente mais ricas para a investigação.

### ✅ Etapas Finalizadas
1.  **ETL - Camada Trusted**: O script `trusted_zone.py` executou a limpeza e padronização dos dados brutos. Suas principais ações foram a aplicação de **regras de negócio condicionais** para tratar campos vazios e a criação de um **valor sentinela (`-100`)** para diferenciar "não preenchimento esperado" de um dado genuinamente ausente.
2.  **ETL - Camada Refined (Análise de Completude)**: A partir da camada `Trusted`, o script `refined_zone_for_null_analysis.py` executou uma profunda transformação nos dados. A principal operação foi o **`melt`** (ou unpivot), que converteu a tabela de um formato largo para um formato longo. Com isso, cada linha passou a representar uma única variável de uma escola, facilitando a análise no Power BI. Para lidar com o grande volume de dados de forma eficiente, o processo foi otimizado para baixo uso de memória através de:
    * Leitura do arquivo de origem em `chunks` (pedaços).
    * Escrita incremental do resultado diretamente em um arquivo **Parquet**, utilizando a biblioteca `PyArrow`.
3.  **Visualização de Dados**: Os principais achados da análise de completude foram consolidados em um dashboard interativo.

### 🚧 Etapas Em Desenvolvimento
4.  **ETL - Camada Refined (Análise de Inconsistências)**: Uma terceira etapa de ETL preparará os dados para a análise de cruzamentos, facilitando a identificação de contradições lógicas entre os campos preenchidos.
5.  **Análise e Diagnóstico**: A análise dos dados de inconsistência será conduzida em `Jupyter Notebooks`.
6.  **Visualização de Dados**: Os principais achados da análise de inconsistências serão consolidados em um segundo dashboard interativo.

---
## ✅ Validação e Qualidade do ETL
Para garantir a integridade dos dados após a complexa transformação de `melt` (que expandiu a base para mais de 90 milhões de linhas), foi criado um script de verificação: `etl_verification_trusted-refined_melted.py`.

Este script compara a contagem de **escolas únicas (`CO_ENTIDADE`)** entre a camada `Trusted` (origem) e a `Refined` (resultado). Ao confirmar que os números são idênticos, o script valida que nenhuma escola foi perdida ou indevidamente duplicada durante o processo de ETL, garantindo a confiabilidade da base de dados usada para a análise.

---
## 📊 Dashboard Interativo no Power BI
Os resultados da análise foram compilados em um painel interativo no Power BI, que permite a exploração visual dos dados de completude e inconsistência por região, dependência administrativa e outras variáveis.

> **[Clique aqui para ver os detalhes e a análise do dashboard](./powerbi/analise_dashboard.md)**

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.9
* **Bibliotecas de Dados:** Pandas, Numpy, PyArrow
* **Visualização (Análise):** Matplotlib, Seaborn
* **Dashboarding:** Power BI Desktop

---

## 🚀 Como Executar o Projeto
1.  Clone este repositório:
    ```bash
    git clone https://github.com/felipecsr/qualidade_dados_censo_escolar_2024.git
    ```
2.  Navegue até o diretório do projeto:
    ```bash
    cd qualidade_dados_censo_escolar_2024
    ```
3.  Instale as dependências (recomenda-se o uso de um ambiente virtual):
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute os scripts de ETL na ordem correta, dentro da pasta `scripts/`:
    * `python trusted_zone.py`
    * `python refined_zone_for_null_analysis.py`
    * (Opcional, mas recomendado) `python etl_verification_trusted-refined_melted.py`
    * (Em breve) `python refined_zone_for_inconsistency_analysis.py`
5.  Abra os notebooks na pasta `notebooks/` para ver a análise detalhada.

---

## 📂 Organização do repositório
- `data/`: Contém as bases de dados nas camadas `raw`, `trusted` e `refined`.
- `scripts/`: Armazena os pipelines em Python para a criação das camadas de dados.
- `notebooks/`: Análises exploratórias e estatísticas desenvolvidas em Jupyter.
- `powerbi/`: Arquivo `.pbix` do Power BI e o markdown com a análise dos dashboards.
- `README.md`: Esta apresentação do projeto.