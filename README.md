# 🧪 Qualidade dos Dados no Censo Escolar 2024

### Uma análise da completude e de potenciais inconsistências nos microdados da educação básica

---

## 💥 Problemática real para inspirar o projeto
Artigo publicado por Guilherme Lichand em 28/12/2023, para o Nexo Jornal: 
[O que uma nova pesquisa revela sobre desiguladades invisíveis no Ensino Básico brasileiro](https://pp.nexojornal.com.br/ponto-de-vista/2023/11/17/o-que-uma-nova-pesquisa-revela-sobre-desigualdades-invisiveis-no-ensino-basico-brasileiro)

E também uma reportagem de Laura Mattos para a Folha de São Paulo, publicada em 21/08/2024, novamente com participação do Guilherme Lichand: 
[Brasil tem 3,5 vezes mais alunos com deficiência do que indicam dados oficiais, diz pesquisa](https://www1.folha.uol.com.br/educacao/2024/08/brasil-tem-35-vezes-mais-alunos-com-deficiencia-do-que-indicam-dados-oficiais-diz-pesquisa.shtml)


---

## 📌 Contexto e situação-problema
O Censo Escolar é a principal base de dados sobre a educação básica brasileira. Utilizado para formulação de políticas, repasses de recursos e diagnóstico de desigualdades, ele assume que os dados coletados refletem com precisão a realidade das escolas.
Entretanto, estudos recentes — como os conduzidos pela equipe do **Equidade.info** — têm mostrado que **há discrepâncias relevantes entre os dados autodeclarados e a realidade observada por pesquisas de campo**. A falta de informação ou o preenchimento impreciso podem comprometer decisões públicas e invisibilizar desigualdades.

---

## 🎯 Objetivo

Este projeto tem como objetivo **analisar a qualidade dos microdados do Censo Escolar 2024**, a partir de dois eixos principais:
1. **Missing Data**: investigar padrões de ausência de preenchimento por tipo de variável.
2. **Potenciais inconsistências**: identificar cruzamentos entre variáveis que podem sugerir sinais de contradição ou distorção.

OBS: ambos objetivos terão suas distribuições observadas por rede de ensino, região e perfil da escola, afim de tentar tangibilizar se há perfil ou tratam-se de questões sistêmicas dna coleta do Censo.

---

## 🔬 Etapas do Projeto

1. **ETL com criação de camadas Trusted e Refined**: SQL/ Dbeaver (SQLite) e Python (pandas) 
3. **Análise de completude geral e por campo**: Jupyter Notebook (pandas, numpy, matplotlib, seaborn)
4. **Levantamento de cruzamentos com potencial de inconsistência**: Jupyter Notebook (pandas, numpy, matplotlib, seaborn)
5. **Visualizações com foco exploratório e narrativo**: Power BI

---

## 📂 Organização do repositório

- `data/`: bases nas camadas raw, trusted e refined
- `scripts/`: pipelines em SQL e Python
- `notebooks/`: análises exploratórias e visuais
- `powerbi/`: dashboards e relatórios
- `README.md`: esta apresentação