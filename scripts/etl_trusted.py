import pandas as pd
import os
import time
from datetime import datetime

# Caminhos (ajuste para seu ambiente)
RAW_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/1_raw/microdados_ed_basica_2024.csv"
TRUSTED_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/2_trusted/microdados_ed_basica_trusted.csv"
DICT_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/1_raw/dicionario.csv"
LOG_PATH = TRUSTED_PATH.replace(".csv", "_log.txt")

def log(msg):
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg)

# Timer - início
start_time = time.time()
start_dt = datetime.now()
os.makedirs(os.path.dirname(TRUSTED_PATH), exist_ok=True)

log("=== ETL Trusted - Execução iniciada ===")
log(f"Início: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")

# 1. Leitura do dicionário de dados
df_dict = pd.read_csv(DICT_PATH, sep=",", quotechar='"', on_bad_lines='skip', header=0)
print(df_dict.columns.tolist())
df_dict = df_dict.rename(columns=lambda x: x.strip())
df_dict = df_dict.dropna(subset=["Nome da Variável"]).reset_index(drop=True)

# Listas automáticas (do dicionário)
cols_texto = df_dict[df_dict["Tipo"] == "Char"]["Nome da Variável"].tolist()
cols_data = df_dict[df_dict["Tipo"] == "Data"]["Nome da Variável"].tolist()
cols_binario = df_dict[df_dict["Nome da Variável"].str.startswith("IN_")]["Nome da Variável"].tolist()
# Acrescenta flags tipo Num com "0 - Não" e "1 - Sim"
mask_flag = (
    (df_dict["Tipo"] == "Num") &
    df_dict["Categoria"].fillna("").str.contains("0 - Não", na=False) &
    df_dict["Categoria"].fillna("").str.contains("1 - Sim", na=False)
)
cols_flag_extra = df_dict[mask_flag]["Nome da Variável"].tolist()
cols_binario = list(sorted(set(cols_binario + cols_flag_extra)))

log(f"Variáveis textuais (Char): {len(cols_texto)} colunas")
log(f"Variáveis datas: {len(cols_data)} colunas")
log(f"Variáveis binárias/flags: {len(cols_binario)} colunas")

# 2. Leitura da RAW
df = pd.read_csv(RAW_PATH, encoding="utf-8", sep=";", dtype=str)
n_linhas_raw = len(df)
log(f"Linhas lidas da base RAW: {n_linhas_raw}")

# 3. Padronização textual
n_texto_tratado = 0
for col in cols_texto:
    if col in df.columns:
        before_na = df[col].isna().sum()
        df[col] = df[col].astype(str).str.strip().str.upper()
        after_na = df[col].isna().sum()
        n_texto_tratado += len(df) - before_na
log(f"Padronização textual aplicada às colunas: {cols_texto}")

# 4. Conversão de campos binários
binario_contadores = {
    "total": 0,
    "para_null": 0,
    "para_int": 0,
    "mantidos": 0
}
def trata_binario(x):
    binario_contadores["total"] += 1
    if pd.isna(x) or x == "" or str(x).lower() == "nan":
        binario_contadores["para_null"] += 1
        return pd.NA
    if str(x) == "0":
        binario_contadores["para_int"] += 1
        return 0
    if str(x) == "1":
        binario_contadores["para_int"] += 1
        return 1
    binario_contadores["mantidos"] += 1
    return x  # mantém valor original

for col in cols_binario:
    if col in df.columns:
        df[col] = df[col].apply(trata_binario)
log(f"Tratamento campos binários ({len(cols_binario)} colunas):")
log(f"  - Total de campos processados: {binario_contadores['total']}")
log(f"  - Convertidos para inteiro (0/1): {binario_contadores['para_int']}")
log(f"  - Convertidos para null (vazios/Nan): {binario_contadores['para_null']}")
log(f"  - Mantidos sem alteração (outros valores): {binario_contadores['mantidos']}")

# 5. Padronização datas
n_datas_nulas = 0
for data_col in cols_data:
    if data_col in df.columns:
        before_na = df[data_col].isna().sum()
        df[data_col] = pd.to_datetime(df[data_col], errors="coerce").dt.date
        after_na = df[data_col].isna().sum()
        n_datas_nulas += after_na - before_na
log(f"Padronização aplicada às datas. Novos valores nulos (NaT) criados: {n_datas_nulas}")

# 6. Remoção de duplicatas
duplicated_mask = df.duplicated(keep='first')
linhas_removidas = df.loc[duplicated_mask, "CO_ENTIDADE"].tolist() if "CO_ENTIDADE" in df.columns else []
n_linhas_duplicadas = len(linhas_removidas)
df = df.drop_duplicates(keep='first')
n_final = len(df)
if n_linhas_duplicadas > 0:
    log(f"Linhas duplicadas removidas: {n_linhas_duplicadas}")
    log(f"Lista de CO_ENTIDADE removidas: {linhas_removidas}")
else:
    log("Nenhuma linha duplicada detectada.")
log(f"Linhas finais após remoção de duplicatas: {n_final}")

# 7. Exporta camada trusted (separador ; conforme solicitado)
df.to_csv(TRUSTED_PATH, index=False, encoding="utf-8", sep=";")
log(f"\nArquivo trusted salvo em: {TRUSTED_PATH}")

# Timer - fim
end_time = time.time()
end_dt = datetime.now()
tempo_total = end_time - start_time
tempo_min = tempo_total / 60
tempo_hr = tempo_total / 3600

log(f"\nFim: {end_dt.strftime('%Y-%m-%d %H:%M:%S')}")
log(f"Tempo total de execução: {tempo_total:.2f} segundos ({tempo_min:.2f} min | {tempo_hr:.2f} h)")

log("=== ETL Trusted - Execução finalizada ===")
