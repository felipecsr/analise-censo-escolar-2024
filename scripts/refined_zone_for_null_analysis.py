import pandas as pd
import numpy as np
import os
import pyarrow as pa
import pyarrow.parquet as pq

# =================================================================
# FASE 1: CONFIGURAÇÃO
# =================================================================
print("Iniciando processo com escrita incremental (ultra otimizado para memória)...")

# --- Caminhos ---
TRUSTED_CSV_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/2_trusted/microdados_ed_basica_trusted.csv"
DICT_CSV_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/1_raw/dicionario.csv"
REFINED_OUTPUT_DIR = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/3_refined"
OUTPUT_FILENAME = "refined_analise_de_nulos_com_id.parquet"
FINAL_OUTPUT_PATH = os.path.join(REFINED_OUTPUT_DIR, OUTPUT_FILENAME)

CHUNKSIZE = 40000 

print("Carregando o dicionário de dados...")
df_dicionario = pd.read_csv(DICT_CSV_PATH, sep=",", on_bad_lines='skip')
df_dicionario.columns = df_dicionario.columns.str.strip()
df_dicionario = df_dicionario.dropna(subset=["VARIAVEL"])
df_dict_subset = df_dicionario[['VARIAVEL', 'GRUPO_CAT', 'SUB_GRUPO_CAT']].drop_duplicates()
print("Dicionário carregado.")


# =================================================================
# FASE 2: PROCESSAMENTO EM CHUNKS E ESCRITA INCREMENTAL
# =================================================================

# Inicializamos o 'escritor' de Parquet como nulo
parquet_writer = None

try:
    csv_reader = pd.read_csv(TRUSTED_CSV_PATH, sep=";", low_memory=False, chunksize=CHUNKSIZE)
    print(f"\nIniciando o processamento e escrita incremental...")

    for i, chunk in enumerate(csv_reader):
        print(f"  -> Processando e salvando chunk {i+1}...")
        
        # Lógica de processamento (melt, merge, classify) - igual a antes
        chunk_long = chunk.melt(id_vars=['CO_ENTIDADE'], var_name='VARIAVEL', value_name='VALOR')
        chunk_merged = pd.merge(chunk_long, df_dict_subset, on='VARIAVEL', how='left')
        chunk_merged['GRUPO_CAT'] = chunk_merged['GRUPO_CAT'].fillna('Sem Grupo')
        chunk_merged['SUB_GRUPO_CAT'] = chunk_merged['SUB_GRUPO_CAT'].fillna('Sem Subgrupo')
        conditions = [chunk_merged['VALOR'].isnull(), chunk_merged['VALOR'] == -100]
        choices = ['Nulo', 'Preenchimento Ambíguo']
        chunk_merged['status'] = np.select(conditions, choices, default='Preenchido')
        chunk_final = chunk_merged[['CO_ENTIDADE', 'GRUPO_CAT', 'SUB_GRUPO_CAT', 'VARIAVEL', 'status']]
        
        # --- Lógica de Escrita Incremental ---
        # Converte o chunk do pandas para uma Tabela Arrow (formato nativo do Parquet)
        table = pa.Table.from_pandas(chunk_final, preserve_index=False)
        
        if parquet_writer is None:
            # No primeiro chunk, criamos o arquivo e inicializamos o escritor
            os.makedirs(REFINED_OUTPUT_DIR, exist_ok=True)
            parquet_writer = pq.ParquetWriter(FINAL_OUTPUT_PATH, table.schema, compression='snappy')
        
        # Escreve a tabela (chunk) atual no arquivo Parquet
        parquet_writer.write_table(table)

finally:
    # Garante que o escritor seja fechado, finalizando o arquivo corretamente
    if parquet_writer:
        parquet_writer.close()
        print("\n--- PROCESSO CONCLUÍDO! Arquivo Parquet final gerado com sucesso. ---")