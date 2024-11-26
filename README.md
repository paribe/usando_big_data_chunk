# Uso de Chunks no Python para Processamento de Grandes Arquivos CSV

Este projeto demonstra como processar grandes arquivos CSV de forma eficiente usando chunks com a biblioteca `pandas` em Python. O objetivo principal é evitar problemas de memória ao lidar com arquivos muito grandes, processando-os em pedaços menores.

## Cenário do Projeto

O arquivo CSV utilizado neste projeto contém os seguintes campos:

- `nome_cliente`: Nome do cliente.
- `endereco_cliente`: Endereço do cliente.
- `dat_vencimento`: Data de vencimento.
- `data_pagamento`: Data de pagamento.
- `data_ultimo_credito`: Data do último crédito.
- `valor_limite`: Limite de valor do cliente.
- `produto_comprado`: Nome do produto comprado.
- `quantidade`: Quantidade comprada.
- `valor_unitario`: Valor unitário do produto.
- `valor_total`: Valor total da compra.
- `data_inclusão`: Data de inclusão do registro.

Com um arquivo que cresce 10% diariamente, processá-lo integralmente em memória pode ser inviável. Usamos o conceito de chunks para processar os dados em pedaços menores e selecionar somente os registros com a data de inclusão correspondente ao dia atual do sistema operacional.

## Como Funciona

O script lê o arquivo CSV em chunks, filtra as linhas desejadas e salva os resultados em um novo arquivo. Os principais passos são:

1. **Divisão do Arquivo em Chunks**:
   - Usamos a funcionalidade `chunksize` do `pandas.read_csv` para carregar o arquivo em partes menores.
   - Esse processo é eficiente e evita consumir toda a memória disponível.

2. **Filtragem por Data**:
   - Apenas os registros com a `data_inclusão` correspondente ao dia atual (formato `YYYY-MM-DD`) são mantidos.
   - As colunas são previamente selecionadas para otimizar o desempenho.

3. **Concatenação dos Resultados**:
   - Após o processamento, os pedaços filtrados são reunidos em um único DataFrame.
   - Os dados podem ser salvos em um novo arquivo CSV ou utilizados diretamente no programa.

## Código de Exemplo

```python
import pandas as pd
from datetime import datetime

# Configuração
arquivo_csv = "cliente_fornecedor.csv"
data_atual = datetime.now().strftime("%Y-%m-%d")
chunk_size = 100000
campos_csv = [
    "nome_cliente", "endereco_cliente", "dat_vencimento", "data_pagamento",
    "data_ultimo_credito", "valor_limite", "produto_comprado",
    "quantidade", "valor_unitario", "valor_total", "data_inclusão"
]
dados_filtrados = []

# Processamento com chunks
for chunk in pd.read_csv(arquivo_csv, chunksize=chunk_size, usecols=campos_csv):
    chunk["data_inclusão"] = pd.to_datetime(chunk["data_inclusão"], errors="coerce").dt.strftime("%Y-%m-%d")
    chunk_filtrado = chunk[chunk["data_inclusão"] == data_atual]
    if not chunk_filtrado.empty:
        dados_filtrados.append(chunk_filtrado)

resultado_final = pd.concat(dados_filtrados, ignore_index=True)
resultado_final.to_csv("resultado_data_atual.csv", index=False)


# Benefícios do Uso de Chunks


- Eficiência de Memória: Apenas uma parte do arquivo é carregada por vez.
- Flexibilidade: Permite processar arquivos grandes em máquinas com recursos limitados.
- Escalabilidade: Pode ser facilmente adaptado para outros cenários, como filtragem por diferentes critérios ou cálculos agregados.

# Requisitos
Python 3.8 ou superior.
Biblioteca pandas.