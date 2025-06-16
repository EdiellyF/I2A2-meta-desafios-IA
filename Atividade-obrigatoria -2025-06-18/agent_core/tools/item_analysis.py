import pandas as pd

def list_top_expensive_items(itens_df: pd.DataFrame, top_n: int = 10) -> str:
    """
    Lista os N produtos/serviços mais caros com base no valor unitário.
    """
    if itens_df.empty:
        return "Dados de itens não disponíveis para listar produtos caros."
    
    # Verificar se as colunas necessárias existem
    required_cols = ['DESCRIÇÃO DO PRODUTO/SERVIÇO', 'VALOR UNITÁRIO']
    if not all(col in itens_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes no dataset de itens. Verifique se '{required_cols[0]}' e '{required_cols[1]}' existem."
    
    try:
        # Converter VALOR UNITÁRIO para numérico, tratando erros
        itens_df['VALOR UNITÁRIO'] = pd.to_numeric(itens_df['VALOR UNITÁRIO'], errors='coerce')
        itens_df.dropna(subset=['VALOR UNITÁRIO'], inplace=True)

        if itens_df.empty:
            return "Não há itens com valor unitário válido para análise."

        # Ordenar por valor unitário e pegar os top N únicos
        top_items = itens_df.sort_values(by='VALOR UNITÁRIO', ascending=False) \
                            .drop_duplicates(subset=['DESCRIÇÃO DO PRODUTO/SERVIÇO']) \
                            .head(top_n)
        
        if top_items.empty:
            return "Nenhum produto/serviço caro encontrado."
        
        report = f"Top {top_n} produtos/serviços mais caros (por valor unitário):\n\n"
        for _, row in top_items.iterrows():
            report += (
                f"- {row['DESCRIÇÃO DO PRODUTO/SERVIÇO']}: R$ {row['VALOR UNITÁRIO']:.2f}\n"
            )
        return report
    except Exception as e:
        return f"Erro ao listar produtos mais caros: {str(e)}"

def list_product_ncm_pairs(itens_df: pd.DataFrame) -> str:
    """
    Lista a descrição do produto/serviço e seu respectivo NCM/SH.
    """
    if itens_df.empty:
        return "Dados de itens não disponíveis para listar descrições e NCMs."

    required_cols = ['DESCRIÇÃO DO PRODUTO/SERVIÇO', 'NCM/SH (TIPO DE PRODUTO)']
    if not all(col in itens_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes no dataset de itens. Verifique se '{required_cols[0]}' e '{required_cols[1]}' existem."

    try:
        # Selecionar as colunas e remover duplicatas para uma lista de pares únicos
        unique_pairs = itens_df[required_cols].drop_duplicates()

        if unique_pairs.empty:
            return "Nenhum par de descrição de produto/NCM encontrado."

        report = "Lista de Descrições de Produtos/Serviços e seus NCM/SH:\n\n"
        for _, row in unique_pairs.iterrows():
            report += (
                f"- Descrição: {row['DESCRIÇÃO DO PRODUTO/SERVIÇO']}\n"
                f"  NCM/SH: {row['NCM/SH (TIPO DE PRODUTO)']}\n\n"
            )
        return report
    except Exception as e:
        return f"Erro ao listar descrições e NCMs: {str(e)}"

def top_products_by_total_quantity(itens_df: pd.DataFrame, top_n: int = 10) -> str:
    if itens_df.empty: return "Dados de itens não disponíveis."
    required_cols = ['DESCRIÇÃO DO PRODUTO/SERVIÇO', 'QUANTIDADE']
    if not all(col in itens_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    
    try:
        itens_df['QUANTIDADE'] = pd.to_numeric(itens_df['QUANTIDADE'], errors='coerce').fillna(0)
        top_products = itens_df.groupby('DESCRIÇÃO DO PRODUTO/SERVIÇO')['QUANTIDADE'].sum().nlargest(top_n).reset_index()
        if top_products.empty: return "Nenhum produto encontrado por quantidade."
        report = f"Top {top_n} Produtos/Serviços por Quantidade Total Acumulada:\n\n"
        for _, row in top_products.iterrows():
            report += f"- {row['DESCRIÇÃO DO PRODUTO/SERVIÇO']}: {row['QUANTIDADE']:.2f}\n"
        return report
    except Exception as e: return f"Erro ao analisar top produtos por quantidade: {str(e)}"

def total_value_by_ncm_code(itens_df: pd.DataFrame, ncm_code: str) -> str:
    if itens_df.empty: return "Dados de itens não disponíveis."
    required_cols = ['CÓDIGO NCM/SH', 'VALOR TOTAL']
    if not all(col in itens_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    
    try:
        itens_df['VALOR TOTAL'] = pd.to_numeric(itens_df['VALOR TOTAL'], errors='coerce').fillna(0)
        filtered_df = itens_df[itens_df['CÓDIGO NCM/SH'].astype(str) == str(ncm_code)]
        total_value = filtered_df['VALOR TOTAL'].sum()
        if filtered_df.empty: return f"Nenhum item encontrado para o CÓDIGO NCM/SH '{ncm_code}'."
        return f"O valor total de todos os itens para o CÓDIGO NCM/SH '{ncm_code}' é R$ {total_value:.2f}."
    except Exception as e: return f"Erro ao calcular valor total por código NCM: {str(e)}"

def avg_item_quantity(itens_df: pd.DataFrame) -> str:
    if itens_df.empty: return "Dados de itens não disponíveis."
    if 'QUANTIDADE' not in itens_df.columns: return "Coluna 'QUANTIDADE' ausente."
    
    try:
        itens_df['QUANTIDADE'] = pd.to_numeric(itens_df['QUANTIDADE'], errors='coerce')
        avg_qty = itens_df['QUANTIDADE'].mean()
        if pd.isna(avg_qty): return "Não foi possível calcular a quantidade média por item."
        return f"A quantidade média por item em todas as notas é {avg_qty:.2f}."
    except Exception as e: return f"Erro ao calcular quantidade média por item: {str(e)}"

def find_zero_unit_value_items(itens_df: pd.DataFrame) -> str:
    if itens_df.empty: return "Dados de itens não disponíveis."
    required_cols = ['DESCRIÇÃO DO PRODUTO/SERVIÇO', 'VALOR UNITÁRIO', 'CHAVE DE ACESSO']
    if not all(col in itens_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    
    try:
        itens_df['VALOR UNITÁRIO'] = pd.to_numeric(itens_df['VALOR UNITÁRIO'], errors='coerce').fillna(0)
        zero_value_items = itens_df[itens_df['VALOR UNITÁRIO'] == 0]
        if zero_value_items.empty: return "Nenhum item encontrado com valor unitário zerado."
        report = "Itens com VALOR UNITÁRIO zerado:\n\n"
        for _, row in zero_value_items.iterrows():
            report += f"- Descrição: {row['DESCRIÇÃO DO PRODUTO/SERVIÇO']}, Chave de Acesso: {row['CHAVE DE ACESSO']}\n"
        return report
    except Exception as e: return f"Erro ao encontrar itens com valor unitário zerado: {str(e)}"

def avg_item_total_value(itens_df: pd.DataFrame) -> str:
    if itens_df.empty: return "Dados de itens não disponíveis."
    if 'VALOR TOTAL' not in itens_df.columns: return "Coluna 'VALOR TOTAL' ausente."
    
    try:
        itens_df['VALOR TOTAL'] = pd.to_numeric(itens_df['VALOR TOTAL'], errors='coerce')
        avg_value = itens_df['VALOR TOTAL'].mean()
        if pd.isna(avg_value): return "Não foi possível calcular o valor total médio por item."
        return f"O valor total médio de um item é R$ {avg_value:.2f}."
    except Exception as e: return f"Erro ao calcular valor total médio por item: {str(e)}"

def find_negative_quantity_items(itens_df: pd.DataFrame) -> str:
    if itens_df.empty: return "Dados de itens não disponíveis."
    required_cols = ['DESCRIÇÃO DO PRODUTO/SERVIÇO', 'QUANTIDADE', 'CHAVE DE ACESSO']
    if not all(col in itens_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    
    try:
        itens_df['QUANTIDADE'] = pd.to_numeric(itens_df['QUANTIDADE'], errors='coerce').fillna(0)
        negative_qty_items = itens_df[itens_df['QUANTIDADE'] < 0]
        if negative_qty_items.empty: return "Nenhum item encontrado com quantidade negativa."
        report = "Itens com QUANTIDADE negativa:\n\n"
        for _, row in negative_qty_items.iterrows():
            report += f"- Descrição: {row['DESCRIÇÃO DO PRODUTO/SERVIÇO']}, Quantidade: {row['QUANTIDADE']}, Chave de Acesso: {row['CHAVE DE ACESSO']}\n"
        return report
    except Exception as e: return f"Erro ao encontrar itens com quantidade negativa: {str(e)}"

def find_inconsistent_item_values(itens_df: pd.DataFrame) -> str:
    if itens_df.empty: return "Dados de itens não disponíveis."
    required_cols = ['QUANTIDADE', 'VALOR UNITÁRIO', 'VALOR TOTAL', 'DESCRIÇÃO DO PRODUTO/SERVIÇO', 'CHAVE DE ACESSO']
    if not all(col in itens_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    
    try:
        itens_df['QUANTIDADE'] = pd.to_numeric(itens_df['QUANTIDADE'], errors='coerce').fillna(0)
        itens_df['VALOR UNITÁRIO'] = pd.to_numeric(itens_df['VALOR UNITÁRIO'], errors='coerce').fillna(0)
        itens_df['VALOR TOTAL'] = pd.to_numeric(itens_df['VALOR TOTAL'], errors='coerce').fillna(0)
        
        # Calcular o valor esperado (com tolerância para floats)
        itens_df['VALOR_CALCULADO'] = itens_df['QUANTIDADE'] * itens_df['VALOR UNITÁRIO']
        inconsistencies = itens_df[abs(itens_df['VALOR TOTAL'] - itens_df['VALOR_CALCULADO']) > 0.01] # Tolerância de 0.01

        if inconsistencies.empty: return "Nenhum item encontrado com inconsistência entre Valor Total e (Quantidade * Valor Unitário)."
        report = "Itens com VALOR TOTAL inconsistente com (QUANTIDADE * VALOR UNITÁRIO):\n\n"
        for _, row in inconsistencies.iterrows():
            report += (
                f"- Descrição: {row['DESCRIÇÃO DO PRODUTO/SERVIÇO']}\n"
                f"  Chave de Acesso: {row['CHAVE DE ACESSO']}\n"
                f"  Quantidade: {row['QUANTIDADE']}\n"
                f"  Valor Unitário: R$ {row['VALOR UNITÁRIO']:.2f}\n"
                f"  Valor Total (informado): R$ {row['VALOR TOTAL']:.2f}\n"
                f"  Valor Total (calculado): R$ {row['VALOR_CALCULADO']:.2f}\n"
                f"  Diferença: R$ {row['VALOR TOTAL'] - row['VALOR_CALCULADO']:.2f}\n\n"
            )
        return report
    except Exception as e: return f"Erro ao encontrar inconsistências em valores de itens: {str(e)}" 