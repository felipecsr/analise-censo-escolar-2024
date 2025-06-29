import pandas as pd
import os
import time
from datetime import datetime
import warnings

# =================================================================
# FASE 1: CONFIGURAÇÃO E CARGA
# =================================================================

# --- CAMINHOS ---
RAW_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/1_raw/microdados_ed_basica_2024.csv"
TRUSTED_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/2_trusted/microdados_ed_basica_trusted.csv"
DICT_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/1_raw/dicionario.csv"
LOG_PATH = TRUSTED_PATH.replace(".csv", "_log.txt")

# --- FUNÇÃO DE LOG ---
def log(msg):
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg)

# --- INÍCIO DA EXECUÇÃO ---
start_time = time.time()
start_dt = datetime.now()
os.makedirs(os.path.dirname(TRUSTED_PATH), exist_ok=True)
if os.path.exists(LOG_PATH): os.remove(LOG_PATH)

log("=== ETL 'Desde o Zero' V2 - Execução iniciada ===")
log(f"Início: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")

# --- CARGA DOS DADOS ---
log("1. Carregando arquivos de dicionário e dados brutos...")
df_dict = pd.read_csv(DICT_PATH, sep=",", quotechar='"', on_bad_lines='skip')
df_dict.columns = df_dict.columns.str.strip()
df_dict = df_dict.dropna(subset=["VARIAVEL"])

# Usamos keep_default_na=False para garantir que strings vazias sejam lidas como '' e não como NaN
df = pd.read_csv(RAW_PATH, encoding="utf-8", sep=";", dtype=str, keep_default_na=False)
log(f"Linhas lidas: {len(df)}")


# =================================================================
# FASE 2: PREPARAÇÃO E LIMPEZA
# =================================================================
log("\n2. Limpando e preparando os dados...")

def is_vazio(series):
    return series.astype(str).str.strip().str.upper().isin(["", "NAN", "NA", "NONE", "NULL"])

colunas_de_condicao = ['TP_DEPENDENCIA', 'IN_PODER_PUBLICO_PARCERIA', 'TP_REGULAMENTACAO', 
                       'IN_LOCAL_FUNC_PREDIO_ESCOLAR', 'IN_LOCAL_FUNC_GALPAO', 'QT_COMPUTADOR', 
                       'IN_INTERNET', 'IN_ESCOLARIZACAO', 'IN_EDUCACAO_INDIGENA', 'IN_EXAME_SELECAO']

for col in colunas_de_condicao:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.split('.').str[0]
log("Colunas de condição foram limpas e normalizadas.")


# =================================================================
# FASE 3: APLICAÇÃO DAS REGRAS DE NEGÓCIO (COMPLETO)
# =================================================================
log("\n3. Aplicando regras de tratamento de vazios...")

regras_preenchimento = df_dict[df_dict["Tratamento para o Campo Não Preenchido"].notna()]

for _, regra in regras_preenchimento.iterrows():
    col = regra["VARIAVEL"]
    tratamento = str(regra["Tratamento para o Campo Não Preenchido"]).strip()
    chave_regra = str(regra.get("Campo de Verificação para PREENCHIMENTO_VAZIO", "")).strip()

    if col not in df.columns:
        continue
    
    mascara_vazio = is_vazio(df[col])
    if not mascara_vazio.any():
        continue
    
    log(f"Processando coluna '{col}'...")
    
    if tratamento == "Sem preenchimento = NULL":
        df.loc[mascara_vazio, col] = pd.NA
    
    # --- Bloco completo com as 12 regras ---
    elif chave_regra == "se TP_DEPENDENCIA = 1 or 2 or 3 = PREENCHIMENTO_VAZIO, else NULL":
        condicao = df['TP_DEPENDENCIA'].isin(['1', '2', '3'])
        df.loc[mascara_vazio & condicao, col] = "PREENCHIMENTO_VAZIO"
        df.loc[mascara_vazio & ~condicao, col] = pd.NA
        
    elif chave_regra == "TP_DEPENDENCIA != 4 - Privada, então NULL, else \"PREENCHIMENTO_VAZIO\"":
        condicao = df['TP_DEPENDENCIA'] != '4'
        df.loc[mascara_vazio & condicao, col] = pd.NA
        df.loc[mascara_vazio & ~condicao, col] = "PREENCHIMENTO_VAZIO"
        
    elif chave_regra == "se IN_PODER_PUBLICO_PARCERIA = 1, NULL, else PREENCHIMENTO_VAZIO":
        condicao = df['IN_PODER_PUBLICO_PARCERIA'] == '1'
        df.loc[mascara_vazio & condicao, col] = pd.NA
        df.loc[mascara_vazio & ~condicao, col] = "PREENCHIMENTO_VAZIO"

    elif chave_regra == "se TP_REGULAMENTACAO = 1 = NULL, else PREENCHIMENTO_VAZIO":
        condicao = df['TP_REGULAMENTACAO'] == '1'
        df.loc[mascara_vazio & condicao, col] = pd.NA
        df.loc[mascara_vazio & ~condicao, col] = "PREENCHIMENTO_VAZIO"
    
    elif chave_regra == "Sem preenchimento = string \"PREENCHIMENTO_VAZIO\"":
        df.loc[mascara_vazio, col] = "PREENCHIMENTO_VAZIO"
        
    elif chave_regra == "se IN_LOCAL_FUNC_PREDIO_ESCOLAR = 1 = NULL, else PREENCHIMENTO_VAZIO":
        condicao = df['IN_LOCAL_FUNC_PREDIO_ESCOLAR'] == '1'
        df.loc[mascara_vazio & condicao, col] = pd.NA
        df.loc[mascara_vazio & ~condicao, col] = "PREENCHIMENTO_VAZIO"

    elif chave_regra == "IN_LOCAL_FUNC_GALPAO = 1 = NULL, else PREENCHIMENTO_VAZIO":
        condicao = df['IN_LOCAL_FUNC_GALPAO'] == '1'
        df.loc[mascara_vazio & condicao, col] = pd.NA
        df.loc[mascara_vazio & ~condicao, col] = "PREENCHIMENTO_VAZIO"

    elif chave_regra == "se QT_COMPUTADOR = 0 \"PREENCHIMENTO_VAZIO\", else NULL":
        condicao = df['QT_COMPUTADOR'] == '0'
        df.loc[mascara_vazio & condicao, col] = "PREENCHIMENTO_VAZIO"
        df.loc[mascara_vazio & ~condicao, col] = pd.NA

    elif chave_regra == "se IN_INTERNET = 1 = NULL, else PREENCHIMENTO_VAZIO":
        condicao = df['IN_INTERNET'] == '1'
        df.loc[mascara_vazio & condicao, col] = pd.NA
        df.loc[mascara_vazio & ~condicao, col] = "PREENCHIMENTO_VAZIO"

    elif chave_regra == "se IN_ESCOLARIZACAO = 1 = NULL, else PREENCHIMENTO_VAZIO":
        condicao = df['IN_ESCOLARIZACAO'] == '1'
        df.loc[mascara_vazio & condicao, col] = pd.NA
        df.loc[mascara_vazio & ~condicao, col] = "PREENCHIMENTO_VAZIO"

    elif chave_regra == "se IN_EDUCACAO_INDIGENA = 1 = NULL, else \"PREENCHIMENTO_VAZIO\"":
        condicao = df['IN_EDUCACAO_INDIGENA'] == '1'
        df.loc[mascara_vazio & condicao, col] = pd.NA
        df.loc[mascara_vazio & ~condicao, col] = "PREENCHIMENTO_VAZIO"

    elif chave_regra == "se IN_EXAME_SELECAO = 1 = NULL, else PREENCHIMENTO_VAZIO":
        condicao = df['IN_EXAME_SELECAO'] == '1'
        df.loc[mascara_vazio & condicao, col] = pd.NA
        df.loc[mascara_vazio & ~condicao, col] = "PREENCHIMENTO_VAZIO"

# =================================================================
# FASE 4: TRANSFORMAÇÕES E CONVERSÕES FINAIS
# =================================================================
log("\n4. Aplicando conversões de tipo e de legenda...")

# <<< NOVA ETAPA: Substituição global de "PREENCHIMENTO_VAZIO" por -100 >>>
log("Substituindo 'PREENCHIMENTO_VAZIO' por -100 em todo o dataset...")
df.replace("PREENCHIMENTO_VAZIO", -100, inplace=True)

# Padronização de colunas de texto
cols_texto = df_dict[df_dict["TIPO_ATUALIZADO"] == "string"]["VARIAVEL"].tolist()
for col in cols_texto:
    if col in df.columns:
        # O -100 aqui será convertido para a string '-100' automaticamente
        # fillna importante para correção de <NA> impressos como string ao invés de nulls de fato, no csv final
        df[col] = df[col].fillna('').astype(str).str.strip().str.upper()

# Conversão para numérico (inteiros e floats)
cols_numericas = df_dict[df_dict["TIPO_ATUALIZADO"].isin(["integer", "float"])]["VARIAVEL"].tolist()
for col in cols_numericas:
    if col in df.columns:
        # A conversão agora é mais simples, pois o replace já foi feito
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Conversão para data
print("Convertendo e padronizando colunas de data...")

# Pega a lista de colunas de data do dicionário
cols_data = df_dict[df_dict["TIPO_ATUALIZADO"] == "date"]["VARIAVEL"].tolist()

# Define o formato de data da sua camada RAW (ex: "12FEB2024:00:00:00")
# Fazemos isso uma vez, fora do loop, para ser mais eficiente.
formato_data_raw = "%d%b%Y:%H:%M:%S"

# Loop para processar cada coluna de data
for col in cols_data:
    if col in df.columns:
        print(f"Processando data: {col}...")
        try:
            # ETAPA 1: LEITURA (lendo o formato especial)
            # Primeiro, garantimos que a coluna é do tipo string para evitar erros.
            # Depois, convertemos para datetime usando o formato que definimos.
            series_com_hora = pd.to_datetime(df[col].astype(str),
                                             format=formato_data_raw,
                                             errors='coerce')

            # ETAPA 2: TRANSFORMAÇÃO (deixando no formato padrão sem hora)
            # Agora que a data foi lida corretamente, extraímos apenas a parte da data.
            df[col] = series_com_hora.dt.date

        except Exception as e:
            # Boa prática: avisar se algo der errado com uma coluna específica
            log.warning(f"Não foi possível processar a coluna de data '{col}'. Erro: {e}")

# Conversão de códigos TP_
def processa_legenda_tp(series, legenda_raw):
    try:
        linhas_legenda = [ item.strip() for item in legenda_raw.replace("\r", "").split("\n") if "-" in item ]
        if not linhas_legenda or (len(linhas_legenda) == 1 and ";" in linhas_legenda[0]):
            linhas_legenda = [ item.strip() for item in legenda_raw.split(";") if "-" in item ]
        
        legenda_dict = {}
        for linha in linhas_legenda:
            idx = linha.find('-')
            if idx != -1:
                k = linha[:idx].strip(); v = linha[idx+1:].strip()
                if k: legenda_dict[k] = v
        
        if legenda_dict:
            return series.astype(str).str.strip().map(legenda_dict).fillna(series)
    except Exception as e:
        log(f"[AVISO] Legenda malformada: {legenda_raw} | Erro: {e}")
    return series

tp_cols = df_dict[df_dict["PREFIXO"] == "TP_"]["VARIAVEL"].unique().tolist()
for col in tp_cols:
    if col in df.columns:
        legenda_raw_series = df_dict[df_dict["VARIAVEL"] == col]["SIGNIFICADO_LEGENDA"]
        if not legenda_raw_series.empty:
            legenda_raw = legenda_raw_series.values[0]
            if pd.notna(legenda_raw):
                df[col] = processa_legenda_tp(df[col], legenda_raw)
log("Conversões finais aplicadas.")


# =================================================================
# FASE 5: FINALIZAÇÃO
# =================================================================
log("\n5. Removendo duplicatas e salvando arquivo final...")

linhas_antes = len(df)
df = df.drop_duplicates(keep='first')
linhas_depois = len(df)
log(f"Linhas duplicadas removidas: {linhas_antes - linhas_depois}")

df.to_csv(TRUSTED_PATH, index=False, encoding="utf-8", sep=";")
log(f"Arquivo trusted salvo em: {TRUSTED_PATH}")

end_time = time.time()
log(f"\nTempo total: {end_time - start_time:.2f}s")
log("=== ETL Trusted Zone - Execução finalizada ===")