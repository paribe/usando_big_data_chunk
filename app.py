import pandas as pd
from datetime import datetime

# Caminho para o arquivo CSV
arquivo_csv = "cliente_fornecedor.csv"

# Data atual do sistema operacional
data_atual = datetime.now().strftime("%Y-%m-%d")

# Tamanho do chunk (ajuste conforme necessário)
chunk_size = 100000

# Lista para armazenar os dados filtrados
dados_filtrados = []

# Campos do arquivo CSV
campos_csv = [
    "nome_cliente",
    "endereco_cliente",
    "dat_vencimento",
    "data_pagamento",
    "data_ultimo_credito",
    "valor_limite",
    "produto_comprado",
    "quantidade",
    "valor_unitario",
    "valor_total",
    "data_inclusão"
]

# Iterar pelo arquivo CSV em chunks
for chunk in pd.read_csv(arquivo_csv, chunksize=chunk_size, usecols=campos_csv):
    # Converter a coluna data_inclusão para o formato de data (se necessário)
    chunk["data_inclusão"] = pd.to_datetime(chunk["data_inclusão"], errors="coerce").dt.strftime("%Y-%m-%d")
    
    # Filtrar os dados pela data atual
    chunk_filtrado = chunk[chunk["data_inclusão"] == data_atual]
    
    # Adicionar os dados filtrados à lista
    if not chunk_filtrado.empty:
        dados_filtrados.append(chunk_filtrado)

# Concatenar todos os chunks filtrados em um único DataFrame
resultado_final = pd.concat(dados_filtrados, ignore_index=True)

# Salvar os resultados em um novo arquivo (opcional)
resultado_final.to_csv("resultado_data_atual.csv", index=False)

print(f"Processamento concluído. {len(resultado_final)} registros encontrados para a data {data_atual}.")
