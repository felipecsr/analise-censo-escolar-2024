import pandas as pd
import pyarrow.parquet as pq
import os

# =================================================================
# FASE 1: CONFIGURAÇÃO DOS CAMINHOS
# =================================================================

# Caminho para o arquivo CSV da camada Trusted
TRUSTED_CSV_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/2_trusted/microdados_ed_basica_trusted.csv"

# Caminho para o arquivo Parquet final da camada Refined
REFINED_PARQUET_PATH = "/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/3_refined/refined_analise_de_nulos_com_id.parquet"


# =================================================================
# FASE 2: VERIFICAÇÃO COM BAIXO USO DE MEMÓRIA
# =================================================================

print("--- INICIANDO SCRIPT DE VERIFICAÇÃO DE INTEGRIDADE (VERSÃO OTIMIZADA) ---")

try:
    # --- PASSO 1: Contar entidades únicas na fonte (Trusted) ---
    # Esta parte já era otimizada e permanece a mesma.
    print(f"\nLendo o arquivo Trusted para contagem: {TRUSTED_CSV_PATH}")
    df_trusted_ids = pd.read_csv(TRUSTED_CSV_PATH, sep=';', usecols=['CO_ENTIDADE'])
    trusted_unique_count = df_trusted_ids['CO_ENTIDADE'].nunique()
    print(f"Número de escolas (CO_ENTIDADE) únicas na camada Trusted: {trusted_unique_count}")

    # --- PASSO 2: Contar entidades únicas no resultado (Refined) de forma otimizada ---
    print(f"\nLendo o arquivo Refined em 'batches' para contagem: {REFINED_PARQUET_PATH}")
    
    # Criamos um conjunto (set) vazio para armazenar os IDs únicos
    refined_unique_ids = set()

    # Abrimos o arquivo Parquet sem carregá-lo na memória
    parquet_file = pq.ParquetFile(REFINED_PARQUET_PATH)

    # Iteramos sobre os "grupos de linhas" do arquivo, lendo apenas a coluna que nos interessa
    for batch in parquet_file.iter_batches(columns=['CO_ENTIDADE']):
        # Extraímos a coluna do batch e adicionamos ao nosso conjunto.
        # O 'set' cuida de garantir que apenas valores únicos sejam guardados.
        refined_unique_ids.update(batch.to_pydict()['CO_ENTIDADE'])
    
    # A contagem final é simplesmente o tamanho do nosso conjunto de IDs únicos
    refined_unique_count = len(refined_unique_ids)
    print(f"Número de escolas (CO_ENTIDADE) únicas na camada Refined: {refined_unique_count}")


    # --- PASSO 3: Comparação Final ---
    print("\n" + "="*50)
    print("--- RESULTADO DA VERIFICAÇÃO ---")
    print("="*50)
    
    if trusted_unique_count == refined_unique_count:
        print(f"✅ SUCESSO! A contagem de entidades únicas é idêntica: {trusted_unique_count}.")
        print("A integridade dos registros foi mantida durante o processo de ETL.")
        print("Você pode prosseguir com confiança para a análise no Power BI.")
    else:
        print(f"🚨 ATENÇÃO! HÁ UMA DIVERGÊNCIA NA CONTAGEM DE ENTIDADES ÚNICAS!")
        print(f"  - Trusted: {trusted_unique_count} entidades únicas")
        print(f"  - Refined: {refined_unique_count} entidades únicas")
        print("   -> Isso indica que registros podem ter sido perdidos ou duplicados no processo.")

except FileNotFoundError as e:
    print(f"\nERRO: Um dos arquivos não foi encontrado. Verifique os caminhos.")
    print(f"Detalhe do erro: {e}")