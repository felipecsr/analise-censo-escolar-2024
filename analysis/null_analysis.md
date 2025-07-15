# 🔬 Análise de Completude de Dados - Censo Escolar 2024

Este documento detalha a análise de completude dos dados do Censo Escolar 2024. A investigação revelou que a percepção de uma alta taxa de dados faltantes (14%) é, na verdade, um **artefato metodológico** explicado por uma única variável: a **situação de funcionamento da escola**.

A análise a seguir demonstra como a inclusão de escolas inativas ("Paralisadas" ou "Extintas") na base de dados padrão distorce a percepção de qualidade e como, ao focar nas escolas em operação, o nível de completude dos dados se mostra excelente.

---
### 🛠️ A Descoberta Central: O Impacto da Situação de Funcionamento

A chave para entender a questão dos dados nulos foi encontrada ao analisar o universo de escolas por sua situação operacional. Um quinto dashboard foi criado para explorar a relação entre o **Porte da Escola** e a **Situação de Funcionamento**.

**Aba 5: Análise por Porte e Situação de Funcionamento**
![Aba5](/powerbi/gifs/aba5.gif)  
*Este dashboard, que cruza o porte com a situação da escola, foi o ponto de virada da análise. Ele revelou que a esmagadora maioria dos nulos se concentrava em escolas sem matrículas, com status "Paralisada" ou "Extinta".*

<br>

A investigação neste painel trouxe os seguintes insights definitivos:

* **Taxa de Nulos em Escolas Inativas:** O subconjunto de escolas com status **"Paralisada" ou "Extinta" apresenta uma taxa de nulos de 83%**.
* **Natureza dos Nulos:** Crucialmente, a análise demonstrou que esses nulos **concentram-se quase que exclusivamente nos dados operacionais** (matrículas, infraestrutura em uso, corpo docente, etc.). Os dados cadastrais básicos (identificação, endereço) dessas escolas permanecem preenchidos, como esperado para um registro histórico.
* **Qualidade nas Escolas Ativas:** Ao aplicar um filtro para analisar apenas as escolas **"Em Atividade"**, a taxa de nulos despenca de 14% para apenas **0,69%**, um nível que indica altíssima qualidade no preenchimento dos dados.

---
### 📉 Evidências Secundárias: Os Padrões "Fantasma"

As explorações iniciais, realizadas antes da descoberta da variável `Situação`, apontavam para padrões geográficos e de localização. Hoje, entendemos que esses padrões eram, em grande parte, "fantasmas" ou "ecos" do fenômeno principal: a concentração de escolas inativas em certas áreas.

**Análise por Região, UF, Localização e Dependência**
![GIFs das Abas 1 a 4](/powerbi/gifs/aba1e2.gif)
![GIFs das Abas 1 a 4](/powerbi/gifs/aba3e4.gif)  
*Estas 4 abas do dashboard, exploram variáveis como: Categorias e Subcategorias que criei a partir das 425 variáveis disponíveis no Censo, Região, UF e Mesoregião, Localidade e Dependências administrativas.*  


* **O "Efeito Rural" Recontextualizado:** A maior taxa de nulos em zonas rurais (23% vs 9% na urbana) pode ser amplamente explicada por uma maior proporção de escolas que foram desativadas nessas áreas.
* **Disparidades Geográficas:** Da mesma forma, estados com taxas de nulos muito altas, como Minas Gerais (29%), provavelmente possuem um número maior de registros de escolas paralisadas ou extintas na base de dados do Censo.

---
## ✅ Conclusão da Análise de Completude

A análise conclui que a qualidade de preenchimento dos dados do Censo Escolar 2024, para as **escolas em funcionamento, é excelente (99,31% de completude)**.

A percepção de uma alta taxa de "dados faltantes" (14%) é uma distorção causada pela metodologia de incluir escolas inativas na base de dados pública. Embora a presença desses registros seja importante para fins históricos e administrativos, é fundamental que os analistas de dados apliquem o filtro de `Situação de Funcionamento = "Em Atividade"` para qualquer análise que busque avaliar a qualidade dos dados ou a realidade operacional da educação básica no Brasil.

A ausência de um aviso explícito sobre o impacto deste filtro nos manuais de uso público pode levar a interpretações equivocadas, e este projeto serve como um estudo de caso sobre a importância de se validar o escopo do universo de dados antes de se tirar conclusões.