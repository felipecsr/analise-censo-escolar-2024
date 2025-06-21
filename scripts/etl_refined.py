import pandas as pd
import os
import time
from datetime import datetime

# ========== 1. Caminhos ==========
TRUSTED_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/2_trusted/microdados_ed_basica_trusted.csv"
DICT_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/1_raw/dicionario.csv"
REFINED_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/3_refined/microdados_ed_basica_refined.csv"
LOG_PATH = REFINED_PATH.replace(".csv", "_log.txt")
os.makedirs(os.path.dirname(REFINED_PATH), exist_ok=True)

# ========== 1b. Função de log ==========
def log(msg):
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg)

# ========== 2. Timer - início ==========
start_time = time.time()
start_dt = datetime.now()
log("=== ETL Refined - Execução iniciada ===")
log(f"Início: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")

# ========== 3. Leitura ==========
log("Lendo CSV trusted...")
df = pd.read_csv(TRUSTED_PATH, encoding="utf-8", sep=";", dtype=str)
log(f"Linhas lidas da base trusted: {len(df)}")
log("Lendo dicionário de variáveis...")
df_dict = pd.read_csv(DICT_PATH, encoding="utf-8", sep=",", dtype=str)
log("Dicionário carregado.\n")

# ========== 4. Listagem dos campos dos cruzamentos ==========
campos_cadastro = [
    "NU_ANO_CENSO", "NO_REGIAO", "CO_REGIAO", "NO_UF", "SG_UF", "CO_UF",
    "NO_MUNICIPIO", "CO_MUNICIPIO", "NO_ENTIDADE", "CO_ENTIDADE"
]
# Lista baseada nas 25 flags
campos_usados_nos_cruzamentos = [
    "IN_LABORATORIO_INFORMATICA", "IN_ENERGIA_REDE_PUBLICA", "TP_LOCALIZACAO",
    "QT_TRANSP_RESP_EST", "QT_TRANSP_RESP_MUN", "TP_DEPENDENCIA",
    "IN_PODER_PUBLICO_PARCERIA", "IN_INF", "IN_BANHEIRO_EI", "IN_BIBLIOTECA",
    "IN_BIBLIOTECA_SALA_LEITURA", "IN_PROF_BIBLIOTECARIO", "QT_PROF_BIBLIOTECARIO",
    "IN_INTERNET", "IN_COMPUTADOR", "IN_ALIMENTACAO", "IN_MED", "QT_DOC_MED",
    "IN_ESP", "IN_SALA_ATENDIMENTO_ESPECIAL", "IN_PROF_COORDENADOR", "QT_PROF_ADMINISTRATIVOS",
    "IN_FUND", "QT_MAT_FUND", "QT_MAT_FUND_AI", "QT_MAT_ESP_CC", "QT_MAT_ESP_CE",
    "IN_ESGOTO_REDE_PUBLICA", "IN_MEDIACAO_EAD", "IN_MEDIACAO_SEMIPRESENCIAL",
    "IN_ACESSIBILIDADE_RAMPAS", "IN_ACESSIBILIDADE_CORRIMAO", "IN_ACESSIBILIDADE_SINALIZACAO",
    "IN_ACESSIBILIDADE_INEXISTENTE", "IN_INF_CRE", "IN_DIURNO", "IN_EQUIP_MULTIMIDIA",
    "IN_EDUCACAO_INDIGENA", "CO_LINGUA_INDIGENA_1", "IN_LABORATORIO_CIENCIAS", "IN_AGUA_POTAVEL",
    "TP_ATIVIDADE_COMPLEMENTAR"
]
log(f"Campos utilizados nos cruzamentos: {len(campos_usados_nos_cruzamentos)}\n")

# Identifica quais desses campos são códigos categóricos (TP_*) a serem convertidos para texto
campos_tp = [c for c in campos_usados_nos_cruzamentos if c.startswith("TP_")]
campos_numericos = [c for c in campos_usados_nos_cruzamentos if c not in campos_tp]

# ========== 5. Gera dicionários de conversão para texto ==========
log(f"Convertendo campos categóricos para texto: {campos_tp}")
dicionarios_categoria = {}
for campo in campos_tp:
    df_map = df_dict[df_dict["Nome da Variável"] == campo]
    if not df_map.empty:
        categoria_str = df_map["Categoria"].values[0]
        if pd.notnull(categoria_str):
            dict_codigo_desc = {}
            for linha in categoria_str.strip().split("\n"):
                if "-" in linha:
                    codigo = linha.split("-")[0].strip()
                    desc = linha.strip()
                    dict_codigo_desc[codigo] = desc
            dicionarios_categoria[campo] = dict_codigo_desc
            if campo in df.columns:
                df[campo + "_TXT"] = df[campo].astype(str).map(dict_codigo_desc)
                df.drop(columns=[campo], inplace=True)
log("Conversão categórica concluída.\n")

# ========== 6. Força INT nos binários e quantitativos ==========
log("Padronizando campos numéricos e binários...")
for campo in campos_numericos:
    if campo in df.columns:
        df[campo] = pd.to_numeric(df[campo], errors="coerce").fillna(0).astype(int)
log("Padronização concluída.\n")

# ========== 7. Cruza de variáveis e cria flags ==========
log("Gerando flags de inconsistência e hipótese...")

# 1. ERR_FLAG_LABINFO_SEM_ENERGIA
df["ERR_FLAG_LABINFO_SEM_ENERGIA"] = (
    (df["IN_LABORATORIO_INFORMATICA"] == 1) & (df["IN_ENERGIA_REDE_PUBLICA"] == 0)
).astype(int)
log("Flag ERR_FLAG_LABINFO_SEM_ENERGIA criada.")

# 2. HIP_FLAG_RURAL_SEM_TRANSP
df["HIP_FLAG_RURAL_SEM_TRANSP"] = (
    (df["TP_LOCALIZACAO_TXT"] == "2 - Rural") & 
    (df["QT_TRANSP_RESP_EST"] == 0) & (df["QT_TRANSP_RESP_MUN"] == 0)
).astype(int)
log("Flag HIP_FLAG_RURAL_SEM_TRANSP criada.")

# 3. ERR_FLAG_PRIVADA_VERBA_PUBLICA
df["ERR_FLAG_PRIVADA_VERBA_PUBLICA"] = (
    (df["TP_DEPENDENCIA_TXT"] == "4 - Privada") & 
    (df["IN_PODER_PUBLICO_PARCERIA"] == 1)
).astype(int)
log("Flag ERR_FLAG_PRIVADA_VERBA_PUBLICA criada.")

# 4. ERR_FLAG_INFANTIL_SEM_BANHEIRO
df["ERR_FLAG_INFANTIL_SEM_BANHEIRO"] = (
    (df["IN_INF"] == 1) & (df["IN_BANHEIRO_EI"] == 0)
).astype(int)
log("Flag ERR_FLAG_INFANTIL_SEM_BANHEIRO criada.")

# 5. HIP_FLAG_BIBLIOTECA_SEM_BIBLIOTECARIO
df["HIP_FLAG_BIBLIOTECA_SEM_BIBLIOTECARIO"] = (
    ((df["IN_BIBLIOTECA"] == 1) | (df["IN_BIBLIOTECA_SALA_LEITURA"] == 1)) &
    ((df["IN_PROF_BIBLIOTECARIO"].fillna(0) == 0) & (df["QT_PROF_BIBLIOTECARIO"].fillna(0) == 0))
).astype(int)
log("Flag HIP_FLAG_BIBLIOTECA_SEM_BIBLIOTECARIO criada.")

# 6. ERR_FLAG_INTERNET_SEM_PC
df["ERR_FLAG_INTERNET_SEM_PC"] = (
    (df["IN_INTERNET"] == 1) & (df["IN_COMPUTADOR"] == 0)
).astype(int)
log("Flag ERR_FLAG_INTERNET_SEM_PC criada.")

# 7. ERR_FLAG_ALIMENTACAO_PRIVADA
df["ERR_FLAG_ALIMENTACAO_PRIVADA"] = (
    (df["TP_DEPENDENCIA_TXT"] == "4 - Privada") & (df["IN_ALIMENTACAO"] == 1)
).astype(int)
log("Flag ERR_FLAG_ALIMENTACAO_PRIVADA criada.")

# 8. ERR_FLAG_MEDIO_SEM_PROF
df["ERR_FLAG_MEDIO_SEM_PROF"] = (
    (df["IN_MED"] == 1) & (df["QT_DOC_MED"] == 0)
).astype(int)
log("Flag ERR_FLAG_MEDIO_SEM_PROF criada.")

# 9. HIP_FLAG_ESP_SEM_SALA_ADAPTADA
df["HIP_FLAG_ESP_SEM_SALA_ADAPTADA"] = (
    (df["IN_ESP"] == 1) & (df["IN_SALA_ATENDIMENTO_ESPECIAL"] == 0)
).astype(int)
log("Flag HIP_FLAG_ESP_SEM_SALA_ADAPTADA criada.")

# 10. ERR_FLAG_DIRETORIA_SEM_EQUIPE
df["ERR_FLAG_DIRETORIA_SEM_EQUIPE"] = (
    (df["IN_PROF_COORDENADOR"] == 1) & (df["QT_PROF_ADMINISTRATIVOS"] == 0)
).astype(int)
log("Flag ERR_FLAG_DIRETORIA_SEM_EQUIPE criada.")

# 11. ERR_FLAG_ETAPA_SEM_ALUNO
df["ERR_FLAG_ETAPA_SEM_ALUNO"] = (
    (df["IN_FUND"] == 1) & (df["QT_MAT_FUND"] == 0)
).astype(int)
log("Flag ERR_FLAG_ETAPA_SEM_ALUNO criada.")

# 12. HIP_FLAG_URBANA_SEM_ESGOTO
df["HIP_FLAG_URBANA_SEM_ESGOTO"] = (
    (df["TP_LOCALIZACAO_TXT"] == "1 - Urbana") & (df["IN_ESGOTO_REDE_PUBLICA"] == 0)
).astype(int)
log("Flag HIP_FLAG_URBANA_SEM_ESGOTO criada.")

# 13. ERR_FLAG_ALIMENTACAO_SEM_AGUA
df["ERR_FLAG_ALIMENTACAO_SEM_AGUA"] = (
    (df["IN_AGUA_POTAVEL"] == 0) & (df["IN_ALIMENTACAO"] == 1)
).astype(int)
log("Flag ERR_FLAG_ALIMENTACAO_SEM_AGUA criada.")

# 14. ERR_FLAG_REMOTO_SEM_INTERNET
df["ERR_FLAG_REMOTO_SEM_INTERNET"] = (
    (df["IN_INTERNET"] == 0) & 
    ((df["IN_MEDIACAO_SEMIPRESENCIAL"] == 1) | (df["IN_MEDIACAO_EAD"] == 1))
).astype(int)
log("Flag ERR_FLAG_REMOTO_SEM_INTERNET criada.")

# 15. HIP_FLAG_PCD_SEM_ACESSIBILIDADE
df["HIP_FLAG_PCD_SEM_ACESSIBILIDADE"] = (
    (df["IN_ACESSIBILIDADE_RAMPAS"] == 0) & 
    (df["IN_ACESSIBILIDADE_SINALIZACAO"] == 0) & 
    (df["IN_ACESSIBILIDADE_CORRIMAO"] == 0) &
    ((df["QT_MAT_ESP_CC"] > 0) | (df["QT_MAT_ESP_CE"] > 0))
).astype(int)
log("Flag HIP_FLAG_PCD_SEM_ACESSIBILIDADE criada.")

# 16. ERR_FLAG_CRECHE_COM_MEDIO
df["ERR_FLAG_CRECHE_COM_MEDIO"] = (
    (df["IN_INF_CRE"] == 1) & (df["IN_MED"] == 1)
).astype(int)
log("Flag ERR_FLAG_CRECHE_COM_MEDIO criada.")

# 17. HIP_FLAG_ATIV_COMP_PARTE_DIA
df["HIP_FLAG_ATIV_COMP_PARTE_DIA"] = (
    (df["TP_ATIVIDADE_COMPLEMENTAR_TXT"].notna()) & 
    (df["TP_ATIVIDADE_COMPLEMENTAR_TXT"] != "0 - Não possui") & 
    (df["IN_DIURNO"] == 1)
).astype(int)
log("Flag HIP_FLAG_ATIV_COMP_PARTE_DIA criada.")

# 18. ERR_FLAG_MULTIMIDIA_SEM_ENERGIA
df["ERR_FLAG_MULTIMIDIA_SEM_ENERGIA"] = (
    (df["IN_ENERGIA_REDE_PUBLICA"] == 0) & (df["IN_EQUIP_MULTIMIDIA"] == 1)
).astype(int)
log("Flag ERR_FLAG_MULTIMIDIA_SEM_ENERGIA criada.")

# 19. HIP_FLAG_RURAL_COM_INTERNET
df["HIP_FLAG_RURAL_COM_INTERNET"] = (
    (df["TP_LOCALIZACAO_TXT"] == "2 - Rural") & (df["IN_INTERNET"] == 1)
).astype(int)
log("Flag HIP_FLAG_RURAL_COM_INTERNET criada.")

# 20. HIP_FLAG_ESTADUAL_ANOS_INICIAIS
df["HIP_FLAG_ESTADUAL_ANOS_INICIAIS"] = (
    (df["TP_DEPENDENCIA_TXT"] == "2 - Estadual") & (df["QT_MAT_FUND_AI"] > 0)
).astype(int)
log("Flag HIP_FLAG_ESTADUAL_ANOS_INICIAIS criada.")

# 21. HIP_FLAG_INDIGENA_SEM_LINGUA
df["HIP_FLAG_INDIGENA_SEM_LINGUA"] = (
    (df["IN_EDUCACAO_INDIGENA"] == 1) & 
    ((df["CO_LINGUA_INDIGENA_1"].isna()) | (df["CO_LINGUA_INDIGENA_1"] == 0))
).astype(int)
log("Flag HIP_FLAG_INDIGENA_SEM_LINGUA criada.")

# 22. HIP_FLAG_FEDERAL_INFANTIL
df["HIP_FLAG_FEDERAL_INFANTIL"] = (
    (df["TP_DEPENDENCIA_TXT"] == "1 - Federal") & (df["IN_INF"] == 1)
).astype(int)
log("Flag HIP_FLAG_FEDERAL_INFANTIL criada.")

# 23. HIP_FLAG_LAB_CIENCIA_SEM_INFO
df["HIP_FLAG_LAB_CIENCIA_SEM_INFO"] = (
    (df["IN_LABORATORIO_CIENCIAS"] == 1) & (df["IN_LABORATORIO_INFORMATICA"] == 0)
).astype(int)
log("Flag HIP_FLAG_LAB_CIENCIA_SEM_INFO criada.")

# 24. HIP_FLAG_ESGOTO_NAO_COM_AGUA
df["HIP_FLAG_ESGOTO_NAO_COM_AGUA"] = (
    (df["IN_ESGOTO_REDE_PUBLICA"] == 0) & (df["IN_AGUA_POTAVEL"] == 1)
).astype(int)
log("Flag HIP_FLAG_ESGOTO_NAO_COM_AGUA criada.")

# 25. ERR_FLAG_CONFLITO_ACESSIBILIDADE
df["ERR_FLAG_CONFLITO_ACESSIBILIDADE"] = (
    ((df["IN_ACESSIBILIDADE_RAMPAS"] == 1) | 
     (df["IN_ACESSIBILIDADE_SINALIZACAO"] == 1) | 
     (df["IN_ACESSIBILIDADE_CORRIMAO"] == 1)) & 
    (df["IN_ACESSIBILIDADE_INEXISTENTE"] == 1)
).astype(int)
log("Flag ERR_FLAG_CONFLITO_ACESSIBILIDADE criada.")

# ========== 8. Score ERR e HIP ==========
df["SCORE_ERR"] = df.filter(like="ERR_FLAG_").sum(axis=1)
df["SCORE_HIP"] = df.filter(like="HIP_FLAG_").sum(axis=1)
log("Scores de inconsistências e hipóteses calculados.\n")

# ========== 9. Seleciona colunas finais ==========
campos_final_txt = [c + "_TXT" if c in campos_tp else c for c in campos_usados_nos_cruzamentos]
flags = [c for c in df.columns if c.startswith("ERR_FLAG_") or c.startswith("HIP_FLAG_")]
colunas_finais = campos_cadastro + campos_final_txt + flags + ["SCORE_ERR", "SCORE_HIP"]
df_final = df[colunas_finais]

# ========== 10. Exporta refined ==========
df_final.to_csv(REFINED_PATH, index=False, encoding="utf-8", sep=";")
log(f"Arquivo salvo em: {REFINED_PATH}")

# ========== 11. Timer - fim ==========
end_time = time.time()
end_dt = datetime.now()
tempo_total = end_time - start_time
tempo_min = tempo_total / 60
tempo_hr = tempo_total / 3600
log(f"\nFim: {end_dt.strftime('%Y-%m-%d %H:%M:%S')}")
log(f"Tempo total de execução: {tempo_total:.2f} segundos ({tempo_min:.2f} min | {tempo_hr:.2f} h)")
log("=== ETL Refined - Execução finalizada ===")
