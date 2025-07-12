# 🗺️ Análise do Dashboard Interativo: Qualidade do Censo Escolar 2024

Este documento detalha os dashboards criados no Power BI para explorar visualmente os resultados da análise de qualidade dos dados do Censo Escolar 2024. O objetivo é expor os principais achados de forma descrita e demonstração do visual através das imagens animadas.

---

## Parte 1: Análise de Completude de Dados

Esta primeira parte do dashboard foca em compreender o impacto do não-preenchimento (`nulos`) e observa se há padrão visível nesse comportamento.

### 🎬 Dashboard em Ação (GIF)

Abaixo, um GIF animado demonstra a interatividade e as principais funcionalidades das 4 abas do dashboard de completude.

**Aba 1: Análise por Categoria e Sub-categoria**

![Aba1](/powerbi/gifs/aba1.gif)

<br>

**Aba 2: Análise por Região e UF**

![Aba2](/powerbi/gifs/aba2.gif))
<br>

**Aba 3: Detalhamento de UF por Mesoregião e Municípios**

![Aba3](/powerbi/gifs/aba3.gif))
<br>

**Aba 4: Análise por Localização e Dependência (com possibilidade de Região, UF, Meso, e Município)**

![Aba4](/powerbi/gifs/aba4.gif))
<br>

### 📊 Principais Achados da Análise de Completude

A exploração interativa dos dados no Power BI permitiu uma investigação profunda sobre os padrões de não preenchimento. A análise seguiu uma abordagem investigativa, partindo de uma visão geral para recortes cada vez mais específicos, o que revelou insights complexos e multifatoriais.

* **Ponto de Partida: A Média Nacional e a Ausência de um Padrão Simples:**
    * A análise inicial, agrupada por categorias e subcategorias de variáveis, não revelou um padrão de comportamento único para os dados nulos. A média nacional de não preenchimento situou-se em 14%. Embora algumas subcategorias tenham apresentado taxas mais altas (até 19%), isso foi geralmente causado por variáveis específicas com alta taxa de nulos esperados, como o campo "complemento de endereço" (67% de nulos), que naturalmente não se aplica a muitos casos e, portanto, não indica um problema de qualidade.

* **A Descoberta de Padrões Geográficos: Regiões e Estados:**
    * Ao mudar o prisma da análise para a dimensão geográfica, um padrão claro começou a emergir. As taxas de valores nulos variam drasticamente entre as regiões do Brasil:

        * Baixo índice de nulos: Regiões Centro-Oeste (7%) e Sul (8%).
        * Alto índice de nulos: Regiões Nordeste (17%) e Sudeste (16%).

    * Essa tendência regional é impulsionada por estados que se destacam com taxas de preenchimento nulo muito acima da média nacional, como Minas Gerais (29%), Rio Grande do Norte (25%), Tocantins (25%) e Piauí (22%). Em contrapartida, o Distrito Federal (3,5%) e o Paraná (4,5%) apresentaram os melhores índices de completude do país.

* **O Fator Decisivo: A Influência da Localização Rural vs. Urbana:**
    * O insight mais revelador da análise foi a identificação da localização da escola como o principal preditor de dados nulos. Nacionalmente, escolas em zonas rurais apresentam uma taxa de 23% de não preenchimento, mais que o dobro da taxa de 9% encontrada em zonas urbanas.

    * Essa disparidade é ainda mais acentuada em certas regiões, como o Sudeste (41% rural vs. 11% urbano) e o Sul (20% rural vs. 5% urbano), explicando em grande parte por que estados como MG possuem taxas tão elevadas.

* **Análise Cruzada: Interação entre Localização e Dependência Administrativa:**
    * Aprofundando a análise, foi possível observar como a localização interage com a dependência administrativa da escola:

        * Contexto Urbano: As escolas privadas lideram o índice de nulos (16%), seguidas pelas municipais (14%).

        * Contexto Rural: O "efeito rural" se mostra mais forte e generalizado. Nele, tanto escolas estaduais (20%), municipais (24%) quanto privadas (25%) apresentam altíssimos índices de não preenchimento. Escolas federais mantêm um baixo índice (2,3%) independentemente da localização.

* **Conclusão da Análise de Completude:**
    * A investigação conclui que o não preenchimento de dados no Censo Escolar não segue um padrão simples, mas é fortemente catalisado pela localização rural. Este fator principal, modulado por características da UF e da dependência administrativa, expõe uma fragilidade sistêmica no método de coleta. Em vez de ser um problema isolado de cada localidade, a alta incidência de nulos nestes contextos sugere que o processo de coleta é rígido e uniforme, falhando em se adaptar e aplicar mecanismos de reforço nas áreas onde a completude é historicamente mais desafiadora. A questão central, portanto, não é apenas onde os dados faltam, mas por que o método de coleta permite que essa lacuna persista de forma tão acentuada nestes estratos.

<br>

---

## Parte 2: Análise de Potenciais Inconsistências (Em Breve)

⏳ *Esta seção será preenchida com a análise e os visuais do segundo eixo do projeto.*

O próximo dashboard explorará cruzamentos de variáveis para identificar inconsistências lógicas nos dados declarados. O objetivo será visualizar a frequência de contradições como:

* Escolas que reportam ter computadores, mas não possuem energia elétrica.
* Escolas que oferecem alimentação, mas não declaram possuir uma cozinha.
* Escolas "em atividade" que não possuem turmas ou matrículas.

> **[Análise de Inconsistências - Em Desenvolvimento]**