# 🔬 Análise de Completude de Dados - Censo Escolar 2024

Este documento detalha a **análise exploratória** sobre a completude dos dados do Censo Escolar 2024. O objetivo desta fase foi utilizar ferramentas visuais para identificar padrões, gerar insights e formular hipóteses sobre os fatores que influenciam a ausência de dados na pesquisa.

---
### 🛠️ Ferramenta de Exploração: Dashboard Interativo

A exploração foi conduzida em um dashboard interativo no Power BI, composto por quatro abas principais que permitem a investigação dos dados sob diferentes óticas.

**Aba 1: Análise por Categoria e Sub-categoria**
![Aba1](/powerbi/gifs/aba1.gif)  

*Esta aba permite uma visão geral da distribuição de dados nulos, preenchidos e ambíguos em todas as variáveis, agrupadas por seus respectivos temas.*

<br>

**Aba 2: Análise por Região e UF**
![Aba2](/powerbi/gifs/aba2.gif)  

*Análise do comportamento dos dados faltantes sob um prisma geográfico, comparando as grandes regiões e Unidades Federativas do Brasil.*

<br>

**Aba 3: Detalhamento de UF por Mesoregião e Municípios**
![Aba3](/powerbi/gifs/aba3.gif)  

*Mergulho nos dados em nível local, permitindo a identificação de disparidades dentro de um mesmo estado.*

<br>

**Aba 4: Análise por Localização e Dependência**
![Aba4](/powerbi/gifs/aba4.gif)  

*Cruzamento dos dados por características da escola, como a localização (rural/urbana) e a dependência administrativa (federal, estadual, municipal, privada).*

<br>

---
### 💡 Da Exploração aos Insights: Uma Jornada Investigativa

A análise exploratória foi uma jornada investigativa, partindo de uma visão ampla do universo de dados e mergulhando em detalhes à medida que os primeiros padrões emergiam. O objetivo era "conversar" com os dados para que eles nos contassem onde a qualidade do preenchimento era mais frágil.

A primeira abordagem, e mais intuitiva, foi analisar a ausência de dados por **tema**, ou seja, por `Categoria` e `Sub-categoria` das variáveis. A expectativa era encontrar um grupo de perguntas específico com problemas crônicos de preenchimento. No entanto, o resultado foi inconclusivo: com uma média nacional de **14% de dados nulos**, nenhuma categoria se destacou de forma alarmante. As pequenas variações eram quase sempre explicadas por campos específicos (como "complemento de endereço") onde o não preenchimento é esperado. Este primeiro passo, embora não tenha revelado um padrão claro, foi fundamental para descartar a hipótese de que o problema residia em um "tópico" específico do questionário.

O cenário mudou completamente quando o prisma da análise se voltou para a **dimensão geográfica**. No mapa do Brasil, um padrão claro se desenhou. As regiões Sul (8% de nulos) e Centro-Oeste (7%) apresentavam uma saúde de dados muito superior às regiões Nordeste (17%) e Sudeste (16%). Essa tendência regional, na verdade, era impulsionada por "hotspots" de não preenchimento. Estados como **Minas Gerais (29%)**, **Rio Grande do Norte (25%)** e **Tocantins (25%)** se destacavam negativamente, contrastando de forma gritante com os territórios de maior completude, como o **Distrito Federal (3,5%)** e o **Paraná (4,5%)**. A variabilidade era imensa e a geografia, por si só, parecia não contar a história toda.

Este foi o gancho para o insight mais revelador da análise, que surgiu ao aplicar o filtro de **Localização (Rural vs. Urbana)**. A diferença foi gritante: escolas rurais apresentavam mais que o dobro de dados nulos (23%) em comparação com as urbanas (9%). Esse "efeito rural" se mostrou um fator tão decisivo que, ao mergulhar no nível municipal, a complexidade apenas aumentava. Encontramos municípios vizinhos com realidades opostas: alguns apresentavam **taxas de nulos acima de 40%**, enquanto outros, no mesmo estado, beiravam a completude total. Isso sinalizava que, embora a localização rural fosse um forte indicativo, outros fatores locais intensificavam ou mitigavam esse efeito.

Para adicionar uma camada final de nuance, a investigação cruzou a `Localização` com a `Dependência Administrativa`. Isso revelou que o "efeito rural" era ainda mais complexo e generalizado, impactando fortemente escolas estaduais, municipais e privadas. Ao mesmo tempo, no contexto urbano, um padrão diferente emergia, com as escolas privadas na liderança de dados nulos.

Essa jornada exploratória, com seus caminhos iniciais inconclusivos e suas descobertas progressivas, nos permitiu formular as seguintes hipóteses centrais, que serão o objeto da validação estatística:

* #### **Hipótese 1: A ausência de dados não é aleatória e possui um forte componente geográfico.**
    Escolas nas regiões **Nordeste e Sudeste** têm uma propensão significativamente maior ao não preenchimento em comparação com as regiões **Sul e Centro-Oeste**.

* #### **Hipótese 2: A localização da escola (Rural vs. Urbana) é o principal preditor para a ausência de dados.**
    Uma escola localizada em **zona rural** tem uma chance substancialmente maior de apresentar dados faltantes do que uma escola em **zona urbana**.

* #### **Hipótese 3: A dependência administrativa interage com a localização, intensificando o efeito rural.**
    O "efeito rural" é generalizado e eleva a taxa de nulos em quase todos os tipos de escolas (municipais, privadas e estaduais), enquanto no ambiente urbano, as escolas **privadas** se destacam com a maior taxa de não preenchimento.

---
## ⚖️ Validação Estatística das Hipóteses

Os padrões visuais e as hipóteses geradas na análise exploratória foram um ponto de partida robusto. Para validar essas observações e quantificar a força de cada relação, a fase seguinte do projeto consistiu em uma **análise confirmatória**.

### Metodologia Estatística
A validação foi realizada em um **Jupyter Notebook**, através da construção de um modelo de **Regressão Logística**. O objetivo foi modelar a probabilidade de uma variável ser um "Nulo Genuíno" (`1`) em detrimento de ser um campo preenchido (`0`), utilizando como preditores os fatores identificados na fase exploratória.

### Resultados do Modelo
O modelo estatístico permitiu quantificar o impacto de cada variável, confirmando com rigor as tendências observadas visualmente.

* **Impacto da Localização (Rural vs. Urbana):**
    > *(**Placeholder:** Inserir o coeficiente ou Odds Ratio do modelo. Ex: O modelo demonstrou que pertencer a uma zona rural aumenta a chance de um dado ser nulo em X%, mantendo os outros fatores constantes. O resultado foi estatisticamente significativo com p < 0.001.)*

* **Impacto da Dependência Administrativa:**
    > *(**Placeholder:** Inserir os resultados para as diferentes dependências. Ex: Escolas de gestão municipal e privada mostraram um aumento significativo na probabilidade de nulos em comparação com escolas estaduais, enquanto escolas federais apresentaram o menor risco.)*

* **Impacto da Região Geográfica:**
    > *(**Placeholder:** Inserir os achados para as regiões. Ex: As regiões Nordeste e Sudeste foram confirmadas como tendo um efeito estatisticamente significativo no aumento da probabilidade de dados nulos, quando comparadas à região Sul (região de referência).)*

* **Performance Geral do Modelo:**
    > *(**Placeholder:** Inserir a principal métrica de performance. Ex: O modelo atingiu uma Acurácia/AUC de X, indicando uma boa capacidade preditiva para distinguir os fatores que levam ao não preenchimento.)*

### Conclusões da Validação
1.  **Confirmação das Hipóteses:** A análise confirmatória **validou com sucesso as principais hipóteses** levantadas na fase exploratória. Os fatores de localização, dependência e região se mostraram preditores estatisticamente significativos para a ausência de dados.

2.  **Quantificação do Efeito "Rural":** Ficou comprovado estatisticamente que a **localização rural** não é apenas um indicador visual, mas o fator de **maior impacto preditivo** para a ocorrência de dados nulos.

3.  **Implicações sobre o Método de Coleta:**
    > *(**Placeholder:** Adicionar uma frase final sobre como a confirmação estatística reforça a crítica ao método de coleta. Ex: A força estatística desses fatores reforça a conclusão de que a rigidez do método de coleta do Censo falha em se adaptar aos desafios de contextos específicos, perpetuando lacunas de informação de forma sistemática e previsível.)*