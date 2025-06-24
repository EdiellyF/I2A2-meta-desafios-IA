import pandas as pd

def validate_nfe_consistency(cabecalho_df: pd.DataFrame, itens_df: pd.DataFrame) -> str:
    """
    Valida a consistência entre o valor total da nota e a soma dos itens.
    Retorna um relatório de divergências ou confirma a consistência.
    """
    if cabecalho_df.empty or itens_df.empty:
        return "Dados de cabeçalho ou itens não disponíveis para validação de consistência."

    # Agrupar itens por 'CHAVE DE ACESSO' e somar 'VALOR TOTAL'
    itens_agregados = itens_df.groupby('CHAVE DE ACESSO')['VALOR TOTAL'].sum().reset_index()
    itens_agregados.rename(columns={'VALOR TOTAL': 'SOMA_ITENS'}, inplace=True)

    # Mesclar com os dados do cabeçalho
    merged_df = pd.merge(
        cabecalho_df,
        itens_agregados,
        on='CHAVE DE ACESSO',
        how='left'
    )

    # Preencher NaN em 'SOMA_ITENS' com 0 para notas sem itens
    merged_df['SOMA_ITENS'].fillna(0, inplace=True)

    # Calcular a diferença
    merged_df['DIFERENCA'] = merged_df['VALOR NOTA FISCAL'] - merged_df['SOMA_ITENS']

    # Identificar divergências (usando uma pequena tolerância para floats)
    divergencias = merged_df[abs(merged_df['DIFERENCA']) > 0.01]

    if divergencias.empty:
        return "Nenhuma divergência encontrada entre o valor total das notas e a soma dos itens."
    else:
        report = "Divergências encontradas entre o Valor Total da Nota e a Soma dos Itens:\n\n"
        for _, row in divergencias.iterrows():
            report += (
                f"- Chave de Acesso: {row['CHAVE DE ACESSO']}\n"
                f"  Valor Total da Nota: R$ {row['VALOR NOTA FISCAL']:.2f}\n"
                f"  Soma dos Itens: R$ {row['SOMA_ITENS']:.2f}\n"
                f"  Diferença: R$ {row['DIFERENCA']:.2f}\n\n"
            )
        return report 