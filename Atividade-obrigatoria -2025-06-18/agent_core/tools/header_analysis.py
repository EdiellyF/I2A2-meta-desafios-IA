import pandas as pd

def analyze_top_emitters_by_value(cabecalho_df: pd.DataFrame, top_n: int = 5) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    required_cols = ['RAZÃO SOCIAL EMITENTE', 'VALOR NOTA FISCAL']
    if not all(col in cabecalho_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    
    try:
        cabecalho_df['VALOR NOTA FISCAL'] = pd.to_numeric(cabecalho_df['VALOR NOTA FISCAL'], errors='coerce').fillna(0)
        top_emitters = cabecalho_df.groupby('RAZÃO SOCIAL EMITENTE')['VALOR NOTA FISCAL'].sum().nlargest(top_n).reset_index()
        if top_emitters.empty: return "Nenhum emitente encontrado."
        report = f"Top {top_n} Razões Sociais Emitentes por Valor Total de Notas Fiscais:\n\n"
        for _, row in top_emitters.iterrows():
            report += f"- {row['RAZÃO SOCIAL EMITENTE']}: R$ {row['VALOR NOTA FISCAL']:.2f}\n"
        return report
    except Exception as e: return f"Erro ao analisar top emitentes por valor: {str(e)}"

def count_notes_by_uf_emitter(cabecalho_df: pd.DataFrame) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    if 'UF EMITENTE' not in cabecalho_df.columns: return "Coluna 'UF EMITENTE' ausente."
    try:
        uf_counts = cabecalho_df['UF EMITENTE'].value_counts().reset_index()
        uf_counts.columns = ['UF EMITENTE', 'Quantidade de Notas']
        if uf_counts.empty: return "Nenhuma UF de emitente encontrada."
        report = "Contagem de Notas Fiscais por UF Emitente:\n\n"
        for _, row in uf_counts.iterrows():
            report += f"- {row['UF EMITENTE']}: {row['Quantidade de Notas']} notas\n"
        return report
    except Exception as e: return f"Erro ao contar notas por UF emitente: {str(e)}"

def avg_note_value_by_municipio_emitter(cabecalho_df: pd.DataFrame) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    required_cols = ['MUNICÍPIO EMITENTE', 'VALOR NOTA FISCAL']
    if not all(col in cabecalho_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    try:
        cabecalho_df['VALOR NOTA FISCAL'] = pd.to_numeric(cabecalho_df['VALOR NOTA FISCAL'], errors='coerce').fillna(0)
        avg_values = cabecalho_df.groupby('MUNICÍPIO EMITENTE')['VALOR NOTA FISCAL'].mean().reset_index()
        avg_values.columns = ['Município Emitente', 'Valor Médio da Nota']
        if avg_values.empty: return "Nenhum município emitente encontrado."
        report = "Valor Médio das Notas Fiscais por Município Emitente:\n\n"
        for _, row in avg_values.iterrows():
            report += f"- {row['Município Emitente']}: R$ {row['Valor Médio da Nota']:.2f}\n"
        return report
    except Exception as e: return f"Erro ao calcular valor médio por município emitente: {str(e)}"

def list_notes_by_cnpj_emitter(cabecalho_df: pd.DataFrame, cnpj: str) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    required_cols = ['CPF/CNPJ Emitente', 'CHAVE DE ACESSO', 'VALOR NOTA FISCAL']
    if not all(col in cabecalho_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    
    try:
        filtered_notes = cabecalho_df[cabecalho_df['CPF/CNPJ Emitente'].astype(str) == str(cnpj)]
        if filtered_notes.empty: return f"Nenhuma nota fiscal encontrada para o CNPJ Emitente '{cnpj}'."
        report = f"Notas Fiscais emitidas por '{cnpj}':\n\n"
        for _, row in filtered_notes.iterrows():
            report += f"- Chave de Acesso: {row['CHAVE DE ACESSO']}, Valor: R$ {row['VALOR NOTA FISCAL']:.2f}\n"
        return report
    except Exception as e: return f"Erro ao listar notas por CNPJ emitente: {str(e)}"

def analyze_top_recipients_by_value(cabecalho_df: pd.DataFrame, top_n: int = 5) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    required_cols = ['NOME DESTINATÁRIO', 'VALOR NOTA FISCAL']
    if not all(col in cabecalho_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    
    try:
        cabecalho_df['VALOR NOTA FISCAL'] = pd.to_numeric(cabecalho_df['VALOR NOTA FISCAL'], errors='coerce').fillna(0)
        top_recipients = cabecalho_df.groupby('NOME DESTINATÁRIO')['VALOR NOTA FISCAL'].sum().nlargest(top_n).reset_index()
        if top_recipients.empty: return "Nenhum destinatário encontrado."
        report = f"Top {top_n} Nomes de Destinatários por Valor Total de Notas Fiscais Recebidas:\n\n"
        for _, row in top_recipients.iterrows():
            report += f"- {row['NOME DESTINATÁRIO']}: R$ {row['VALOR NOTA FISCAL']:.2f}\n"
        return report
    except Exception as e: return f"Erro ao analisar top destinatários por valor: {str(e)}"

def count_notes_by_uf_recipient(cabecalho_df: pd.DataFrame) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    if 'UF DESTINATÁRIO' not in cabecalho_df.columns: return "Coluna 'UF DESTINATÁRIO' ausente."
    try:
        uf_counts = cabecalho_df['UF DESTINATÁRIO'].value_counts().reset_index()
        uf_counts.columns = ['UF Destinatário', 'Quantidade de Notas']
        if uf_counts.empty: return "Nenhuma UF de destinatário encontrada."
        report = "Contagem de Notas Fiscais por UF Destinatário:\n\n"
        for _, row in uf_counts.iterrows():
            report += f"- {row['UF Destinatário']}: {row['Quantidade de Notas']} notas\n"
        return report
    except Exception as e: return f"Erro ao contar notas por UF destinatário: {str(e)}"

def count_notes_by_municipio_recipient(cabecalho_df: pd.DataFrame) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    if 'MUNICÍPIO DESTINATÁRIO' not in cabecalho_df.columns: return "Coluna 'MUNICÍPIO DESTINATÁRIO' ausente."
    try:
        municipio_counts = cabecalho_df['MUNICÍPIO DESTINATÁRIO'].value_counts().reset_index()
        municipio_counts.columns = ['Município Destinatário', 'Quantidade de Notas']
        if municipio_counts.empty: return "Nenhum município destinatário encontrado."
        report = "Contagem de Notas Fiscais por Município Destinatário:\n\n"
        for _, row in municipio_counts.iterrows():
            report += f"- {row['Município Destinatário']}: {row['Quantidade de Notas']} notas\n"
        return report
    except Exception as e: return f"Erro ao contar notas por município destinatário: {str(e)}"

def total_value_by_month(cabecalho_df: pd.DataFrame) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    required_cols = ['DATA EMISSÃO', 'VALOR NOTA FISCAL']
    if not all(col in cabecalho_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    
    try:
        cabecalho_df['DATA EMISSÃO'] = pd.to_datetime(cabecalho_df['DATA EMISSÃO'], errors='coerce')
        cabecalho_df.dropna(subset=['DATA EMISSÃO'], inplace=True)
        cabecalho_df['VALOR NOTA FISCAL'] = pd.to_numeric(cabecalho_df['VALOR NOTA FISCAL'], errors='coerce').fillna(0)

        if cabecalho_df.empty: return "Não há dados de emissão válidos para análise temporal."

        cabecalho_df['ANO_MES'] = cabecalho_df['DATA EMISSÃO'].dt.to_period('M')
        monthly_values = cabecalho_df.groupby('ANO_MES')['VALOR NOTA FISCAL'].sum().sort_index().reset_index()
        
        if monthly_values.empty: return "Nenhum valor total por mês encontrado."
        report = "Valor Total das Notas Fiscais por Mês:\n\n"
        for _, row in monthly_values.iterrows():
            report += f"- {row['ANO_MES']}: R$ {row['VALOR NOTA FISCAL']:.2f}\n"
        return report
    except Exception as e: return f"Erro ao calcular valor total por mês: {str(e)}"

def count_notes_by_specific_date(cabecalho_df: pd.DataFrame, date_str: str) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    if 'DATA EMISSÃO' not in cabecalho_df.columns: return "Coluna 'DATA EMISSÃO' ausente."
    
    try:
        target_date = pd.to_datetime(date_str, errors='coerce')
        if pd.isna(target_date): return f"Formato de data inválido: {date_str}. Use 'YYYY-MM-DD'."

        cabecalho_df['DATA EMISSÃO'] = pd.to_datetime(cabecalho_df['DATA EMISSÃO'], errors='coerce')
        cabecalho_df.dropna(subset=['DATA EMISSÃO'], inplace=True)

        count = cabecalho_df[cabecalho_df['DATA EMISSÃO'].dt.date == target_date.date()].shape[0]
        return f"Foram emitidas {count} notas fiscais no dia {date_str}."
    except Exception as e: return f"Erro ao contar notas por data específica: {str(e)}"

def day_of_week_highest_emission(cabecalho_df: pd.DataFrame) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    if 'DATA EMISSÃO' not in cabecalho_df.columns: return "Coluna 'DATA EMISSÃO' ausente."
    
    try:
        cabecalho_df['DATA EMISSÃO'] = pd.to_datetime(cabecalho_df['DATA EMISSÃO'], errors='coerce')
        cabecalho_df.dropna(subset=['DATA EMISSÃO'], inplace=True)

        if cabecalho_df.empty: return "Não há dados de emissão válidos para análise."

        day_counts = cabecalho_df['DATA EMISSÃO'].dt.day_name(locale='pt_BR').value_counts().reset_index()
        day_counts.columns = ['Dia da Semana', 'Quantidade de Notas']
        
        if day_counts.empty: return "Nenhum dia da semana com emissão de notas encontrado."
        most_common_day = day_counts.iloc[0]
        return f"O dia da semana com o maior número de emissões de notas é {most_common_day['Dia da Semana']} com {most_common_day['Quantidade de Notas']} notas."
    except Exception as e: return f"Erro ao identificar dia da semana de maior emissão: {str(e)}"

def count_notes_by_natureza_operacao(cabecalho_df: pd.DataFrame) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    if 'NATUREZA DA OPERAÇÃO' not in cabecalho_df.columns: return "Coluna 'NATUREZA DA OPERAÇÃO' ausente."
    
    try:
        natureza_counts = cabecalho_df['NATUREZA DA OPERAÇÃO'].value_counts().reset_index()
        natureza_counts.columns = ['Natureza da Operação', 'Quantidade de Notas']
        if natureza_counts.empty: return "Nenhuma natureza da operação encontrada."
        report = "Contagem de Notas Fiscais por Natureza da Operação:\n\n"
        for _, row in natureza_counts.iterrows():
            report += f"- {row['Natureza da Operação']}: {row['Quantidade de Notas']} notas\n"
        return report
    except Exception as e: return f"Erro ao contar notas por natureza da operação: {str(e)}"

def total_value_by_natureza_operacao(cabecalho_df: pd.DataFrame, natureza: str) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    required_cols = ['NATUREZA DA OPERAÇÃO', 'VALOR NOTA FISCAL']
    if not all(col in cabecalho_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    
    try:
        cabecalho_df['VALOR NOTA FISCAL'] = pd.to_numeric(cabecalho_df['VALOR NOTA FISCAL'], errors='coerce').fillna(0)
        filtered_df = cabecalho_df[cabecalho_df['NATUREZA DA OPERAÇÃO'].astype(str).str.contains(natureza, case=False, na=False)]
        total_value = filtered_df['VALOR NOTA FISCAL'].sum()
        if filtered_df.empty: return f"Nenhuma nota fiscal encontrada para a natureza da operação '{natureza}'."
        return f"O valor total das notas fiscais para a natureza da operação '{natureza}' é R$ {total_value:.2f}."
    except Exception as e: return f"Erro ao calcular valor total por natureza da operação: {str(e)}"

def find_negative_value_notes(cabecalho_df: pd.DataFrame) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    required_cols = ['VALOR NOTA FISCAL', 'CHAVE DE ACESSO']
    if not all(col in cabecalho_df.columns for col in required_cols):
        return f"Colunas necessárias ausentes: {', '.join(required_cols)}"
    
    try:
        cabecalho_df['VALOR NOTA FISCAL'] = pd.to_numeric(cabecalho_df['VALOR NOTA FISCAL'], errors='coerce').fillna(0)
        negative_notes = cabecalho_df[cabecalho_df['VALOR NOTA FISCAL'] < 0]
        if negative_notes.empty: return "Nenhuma nota fiscal encontrada com valor total negativo."
        report = "Notas Fiscais com VALOR NOTA FISCAL negativo:\n\n"
        for _, row in negative_notes.iterrows():
            report += f"- Chave de Acesso: {row['CHAVE DE ACESSO']}, Valor: R$ {row['VALOR NOTA FISCAL']:.2f}\n"
        return report
    except Exception as e: return f"Erro ao encontrar notas com valor negativo: {str(e)}"

def find_duplicate_note_numbers(cabecalho_df: pd.DataFrame) -> str:
    if cabecalho_df.empty: return "Dados de cabeçalho não disponíveis."
    if 'NÚMERO' not in cabecalho_df.columns: return "Coluna 'NÚMERO' ausente."
    
    try:
        duplicate_numbers = cabecalho_df[cabecalho_df.duplicated(subset=['NÚMERO'], keep=False)]
        if duplicate_numbers.empty: return "Nenhum número de nota fiscal duplicado encontrado."
        report = "Notas Fiscais com NÚMERO duplicado:\n\n"
        for num, group in duplicate_numbers.groupby('NÚMERO'):
            report += f"- Número: {num}, Chaves de Acesso: {', '.join(group['CHAVE DE ACESSO'].tolist())}\n"
        return report
    except Exception as e: return f"Erro ao encontrar números de nota duplicados: {str(e)}" 