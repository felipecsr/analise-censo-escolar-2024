import pandas as pd
import time
import os

# --- Configuração ---
caminho_dados = '/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/2_trusted/microdados_ed_basica_trusted.csv'
caminho_dicionario = '/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/1_raw/dicionario.csv'
caminho_saida_dir = '/home/fcsr/Documentos/Dbeaver/qualidade_dados_censo_escolar_2024/data/3_refined/refined_unpivoted_parquet_output'
id_unico = 'CO_ENTIDADE'
chunk_size = 50000

# --- Preparação ---
print("Iniciando o processo de transformação em lotes...")
if not os.path.exists(caminho_saida_dir):
    os.makedirs(caminho_saida_dir)
    print(f"Diretório de saída criado em: {caminho_saida_dir}")

print("Carregando o dicionário...")
df_dicionario = pd.read_csv(caminho_dicionario)
print("Dicionário carregado.")

# --- Processamento em Lotes ---
data_reader = pd.read_csv(caminho_dados, sep=';', chunksize=chunk_size, low_memory=False)
is_first_chunk = True

for i, chunk in enumerate(data_reader):
    start_time = time.time()
    print(f"Processando lote {i+1}...")

    df_long = chunk.melt(
        id_vars=[id_unico],
        var_name='VARIAVEL',
        value_name='Valor'
    )

    df_final_chunk = pd.merge(df_long, df_dicionario, on='VARIAVEL', how='left')

    # vvv--- A CORREÇÃO ESTÁ AQUI ---vvv
    # Força a coluna 'Valor' a ser do tipo texto (string) para evitar erros de tipo.
    df_final_chunk['Valor'] = df_final_chunk['Valor'].astype(str)
    # ^^^--- FIM DA CORREÇÃO ---^^^

    nome_arquivo_saida = os.path.join(caminho_saida_dir, f'chunk_{i}.parquet')
    
    # A lógica de salvar permanece a mesma.
    # A partir do Pandas 1.5 e PyArrow, podemos usar o modo de escrita para anexar.
    if is_first_chunk:
        df_final_chunk.to_parquet(nome_arquivo_saida, index=False, engine='pyarrow')
        is_first_chunk = False
    else:
        # Nota: a maneira mais segura de anexar é em arquivos diferentes numa pasta,
        # como já estamos fazendo. Se precisássemos de um arquivo único, a lógica mudaria.
        df_final_chunk.to_parquet(nome_arquivo_saida, index=False, engine='pyarrow')

    print(f"--- Lote {i+1} processado e salvo em {time.time() - start_time:.2f} segundos. Arquivo: {nome_arquivo_saida}")

print("\nPROCESSO FINALIZADO COM SUCESSO!")
print(f"Todos os lotes foram salvos no diretório: {caminho_saida_dir}")