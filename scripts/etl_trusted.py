import pandas as pd               # biblioteca principal para manipulação de dados tabulares
import os                         # para manipulação de diretórios e caminhos de arquivos
import time                       # para medir tempo de execução
from datetime import datetime     # para registrar data/hora de início
import warnings                   # para exibir alertas sem interromper o fluxo


# Define os caminhos dos arquivos usados no processo
RAW_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/1_raw/microdados_ed_basica_2024.csv"
TRUSTED_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/2_trusted/microdados_ed_basica_trusted.csv"
DICT_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/1_raw/dicionario.csv"
LOG_PATH = TRUSTED_PATH.replace(".csv", "_log.txt")  # log da execução


# Função para registrar mensagens tanto no terminal quanto em arquivo de log
def log(msg):
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg)

# Função robusta para detectar campos vazios, mesmo quando são strings como "nan", "na", "none", etc.
def is_vazio(valor):
    return pd.isna(valor) or str(valor).strip().upper() in ["", "NAN", "NA", "NONE"]


# Cada função abaixo representa uma regra específica que define quando um campo deve ser
# interpretado como "PREENCHIMENTO_VAZIO" ou como valor ausente (NULL = pd.NA)
def regra_01(r): return "PREENCHIMENTO_VAZIO" if r.get("TP_DEPENDENCIA") in ["1", "2", "3"] else pd.NA
def regra_02(r): return pd.NA if r.get("TP_DEPENDENCIA") != "4" else "PREENCHIMENTO_VAZIO"
def regra_03(r): return pd.NA if r.get("IN_PODER_PUBLICO_PARCERIA") == "1" else "PREENCHIMENTO_VAZIO"
def regra_04(r): return pd.NA if r.get("TP_REGULAMENTACAO") == "1" else "PREENCHIMENTO_VAZIO"
def regra_05(r): return "PREENCHIMENTO_VAZIO"
def regra_06(r): return pd.NA if r.get("IN_LOCAL_FUNC_PREDIO_ESCOLAR") == "1" else "PREENCHIMENTO_VAZIO"
def regra_07(r): return pd.NA if r.get("IN_LOCAL_FUNC_GALPAO") == "1" else "PREENCHIMENTO_VAZIO"
def regra_08(r): return "PREENCHIMENTO_VAZIO" if r.get("QT_COMPUTADOR") == "0" else pd.NA
def regra_09(r): return pd.NA if r.get("IN_INTERNET") == "1" else "PREENCHIMENTO_VAZIO"
def regra_10(r): return pd.NA if r.get("IN_ESCOLARIZACAO") == "1" else "PREENCHIMENTO_VAZIO"
def regra_11(r): return pd.NA if r.get("IN_EDUCACAO_INDIGENA") == "1" else "PREENCHIMENTO_VAZIO"
def regra_12(r): return pd.NA if r.get("IN_EXAME_SELECAO") == "1" else "PREENCHIMENTO_VAZIO"

regras_dict = {
    "se TP_DEPENDENCIA = 1 or 2 or 3 = PREENCHIMENTO_VAZIO, else NULL": regra_01,
    "TP_DEPENDENCIA != 4 - Privada, então NULL, else \"PREENCHIMENTO_VAZIO\"": regra_02,
    "se IN_PODER_PUBLICO_PARCERIA = 1, NULL, else PREENCHIMENTO_VAZIO": regra_03,
    "se TP_REGULAMENTACAO = 1 = NULL, else PREENCHIMENTO_VAZIO": regra_04,
    "Sem preenchimento = string \"PREENCHIMENTO_VAZIO\"": regra_05,
    "se IN_LOCAL_FUNC_PREDIO_ESCOLAR = 1 = NULL, else PREENCHIMENTO_VAZIO": regra_06,
    "IN_LOCAL_FUNC_GALPAO = 1 = NULL, else PREENCHIMENTO_VAZIO": regra_07,
    "se QT_COMPUTADOR = 0 \"PREENCHIMENTO_VAZIO\", else NULL": regra_08,
    "se IN_INTERNET = 1 = NULL, else PREENCHIMENTO_VAZIO": regra_09,
    "se IN_ESCOLARIZACAO = 1 = NULL, else PREENCHIMENTO_VAZIO": regra_10,
    "se IN_EDUCACAO_INDIGENA = 1 = NULL, else \"PREENCHIMENTO_VAZIO\"": regra_11,
    "se IN_EXAME_SELECAO = 1 = NULL, else PREENCHIMENTO_VAZIO": regra_12,
}

# Converte códigos (ex: TP_LOCALIZACAO = "1") para textos legíveis com base na legenda
def processa_legenda_tp(col, legenda_raw, df):
    try:
        # Separa cada item da legenda por quebra de linha OU por ponto e vírgula
        linhas_legenda = [
            item.strip()
            for item in legenda_raw.replace("\r", "").split("\n")  # quebra de linha padrão
            if "-" in item  # ignora linhas sem código - descrição
        ]
        if len(linhas_legenda) <= 1:
            # fallback: tenta split por ponto e vírgula, caso seja a outra formatação
            linhas_legenda = [
                item.strip()
                for item in legenda_raw.split(";")
                if "-" in item
            ]

        # Monta o dicionário de mapeamento: {"1": "Federal", "2": "Estadual", ...}
        legenda_dict = {
            k.strip(): v.strip()
            for k, v in (linha.split(" - ", 1) for linha in linhas_legenda)
        }

        # Aplica a substituição no DataFrame
        df[col] = df[col].astype(str).str.strip().map(legenda_dict).fillna(df[col])

    except Exception:
        warnings.warn(f"[TP_] Legenda malformada para {col}: {legenda_raw}")
        log(f"[TP_] Legenda malformada para {col}: {legenda_raw}")
    
    return df

# Substitui "PREENCHIMENTO_VAZIO" por -100 e converte para numérico
def trata_campo_numerico(col, df):
    df[col] = df[col].replace("PREENCHIMENTO_VAZIO", -100)
    return pd.to_numeric(df[col], errors='coerce')

# =======================
# Execução principal
# =======================

# Marca o início da contagem de tempo (para medir performance)
start_time = time.time()
start_dt = datetime.now()
# Garante que a pasta onde o arquivo final será salvo exista (cria, se necessário)
os.makedirs(os.path.dirname(TRUSTED_PATH), exist_ok=True)
# Inicia o log de execução
log("=== ETL Trusted - Execução iniciada ===")
log(f"Início: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")

# =======================
# Leitura do dicionário
# =======================

# Lê o dicionário de variáveis que contém metadados do Censo Escolar
log("Lendo dicionário de dados...")
df_dict = pd.read_csv(DICT_PATH, sep=",", quotechar='"', on_bad_lines='skip')

# Remove espaços extras dos nomes de colunas
df_dict.columns = df_dict.columns.str.strip()

# Remove linhas sem nome de variável
df_dict = df_dict.dropna(subset=["VARIAVEL"])

# Remove espaços extras nos nomes das variáveis
df_dict["VARIAVEL"] = df_dict["VARIAVEL"].str.strip()

# Padroniza o tipo informado no dicionário para minúsculas, evitando erro por capitalização
df_dict["TIPO_ATUALIZADO"] = df_dict["TIPO_ATUALIZADO"].str.strip().str.lower()

# =======================
# Separação de colunas por tipo
# =======================

# Cria listas separadas com nomes das variáveis do tipo:
# - string (texto)
# - date (datas)
# - integer (números inteiros)
# - float (números decimais)
cols_texto = df_dict[df_dict["TIPO_ATUALIZADO"] == "string"]["VARIAVEL"].tolist()
cols_data = df_dict[df_dict["TIPO_ATUALIZADO"] == "date"]["VARIAVEL"].tolist()
cols_int = df_dict[df_dict["TIPO_ATUALIZADO"] == "integer"]["VARIAVEL"].tolist()
cols_float = df_dict[df_dict["TIPO_ATUALIZADO"] == "float"]["VARIAVEL"].tolist()


# =======================
# Regras para tratamento de campos não preenchidos
# =======================

# Filtra apenas as variáveis que possuem alguma regra de preenchimento especificada
regras_preenchimento = df_dict[
    df_dict["Tratamento para o Campo Não Preenchido"].notna()
][[
    "VARIAVEL", 
    "Tratamento para o Campo Não Preenchido", 
    "Campo de Verificação para PREENCHIMENTO_VAZIO"
]]

# =======================
# Leitura da base RAW
# =======================

# Lê o arquivo de entrada (camada RAW), mantendo todos os dados como strings inicialmente
log("Lendo base RAW...")
df = pd.read_csv(RAW_PATH, encoding="utf-8", sep=";", dtype=str)
log(f"Linhas lidas: {len(df)}")

# =======================
# Aplicação das regras de preenchimento
# =======================

log("Aplicando regras de preenchimento vazio...")

# Para cada variável com regra definida, aplica o tratamento necessário
for _, row_dict in regras_preenchimento.iterrows():
    col = row_dict["VARIAVEL"]
    trat = str(row_dict["Tratamento para o Campo Não Preenchido"]).strip()
    chave_regra = str(row_dict["Campo de Verificação para PREENCHIMENTO_VAZIO"]).strip()

    # Se a coluna não existe no DataFrame, ignora
    if col not in df.columns:
        continue

    # Regra simples: vazio vira NULL
    if trat == "Sem preenchimento = NULL":
        df[col] = df[col].replace("", pd.NA)

    # Regra condicional: vazio pode virar 'PREENCHIMENTO_VAZIO'
    elif trat == "Sem preenchimento = string 'PREENCHIMENTO_VAZIO'":
        if chave_regra in regras_dict:
            funcao_regra = regras_dict[chave_regra]
            df[col] = df.apply(
                lambda r: funcao_regra(r) if is_vazio(r[col]) else r[col],
                axis=1
            )
        else:
            warnings.warn(f"Regra não encontrada: {chave_regra}")
            log(f"[AVISO] Regra não encontrada para {col}: {chave_regra}")

# =======================
# Padronizações por tipo
# =======================

# 🔤 Padroniza campos de texto: remove espaços, converte para maiúsculas
for col in cols_texto:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.upper()
log(f"Padronização textual aplicada a {len(cols_texto)} colunas")

# 🔢 Converte campos numéricos (inteiros e floats)
for col in cols_int:
    if col in df.columns:
        df[col] = trata_campo_numerico(col, df)
for col in cols_float:
    if col in df.columns:
        df[col] = trata_campo_numerico(col, df)
log(f"Conversão aplicada a campos numéricos (int/float)")

# 📆 Converte campos de data
for col in cols_data:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
log(f"Padronização de datas aplicada a {len(cols_data)} colunas")

# =======================
# Conversão de códigos TP_
# =======================

# Identifica todas as variáveis com prefixo "TP_" para substituir códigos por descrições
tp_cols = df_dict[df_dict["PREFIXO"] == "TP_"]["VARIAVEL"].unique().tolist()

for col in tp_cols:
    legenda_raw = df_dict[df_dict["VARIAVEL"] == col]["SIGNIFICADO_LEGENDA"].values
    if len(legenda_raw) > 0 and col in df.columns:
        legenda = legenda_raw[0]
        if pd.notna(legenda):
            df = processa_legenda_tp(col, legenda, df)
log(f"Conversão de códigos TP_ realizada para {len(tp_cols)} colunas")

# =======================
# Remoção de duplicatas
# =======================

# Verifica linhas duplicadas (considerando todas as colunas)
duplicated_mask = df.duplicated(keep='first')

# Salva os IDs das linhas duplicadas (se houver a coluna CO_ENTIDADE)
linhas_removidas = df.loc[duplicated_mask, "CO_ENTIDADE"].tolist() if "CO_ENTIDADE" in df.columns else []

# Remove as duplicadas, mantendo a primeira ocorrência
df = df.drop_duplicates(keep='first')
log(f"Linhas duplicadas removidas: {len(linhas_removidas)}")

# =======================
# Salvando o resultado
# =======================

# Exporta o DataFrame final para a camada trusted
df.to_csv(TRUSTED_PATH, index=False, encoding="utf-8", sep=";")
log(f"Arquivo trusted salvo em: {TRUSTED_PATH}")

# Marca o tempo total da execução
end_time = time.time()
log(f"Tempo total: {end_time - start_time:.2f}s")
log("=== ETL Trusted - Execução finalizada ===")
