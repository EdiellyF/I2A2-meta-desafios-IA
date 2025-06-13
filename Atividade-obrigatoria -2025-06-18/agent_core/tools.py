from typing import List, Callable
from langchain.tools import Tool
import pandas as pd
import os
import logging

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_tools(temp_dir: str, find_data_files: Callable[[str], List[str]]) -> List[Tool]:
    """
    Retorna a lista de ferramentas disponíveis para o agente.
    """
    def analyze_data(query: str) -> str:
        """
        Analisa os dados com base na query fornecida.
        """
        logger.info(f"Iniciando análise com query: {query}")
        files = find_data_files(temp_dir)
        if not files:
            logger.warning("Nenhum arquivo encontrado para análise")
            return "Nenhum arquivo encontrado para análise."

        results = []
        for file in files:
            try:
                logger.info(f"Processando arquivo: {file}")
                file_path = os.path.join(temp_dir, file)
                
                # Lê o arquivo
                if file.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file_path)
                else:
                    continue

                logger.info(f"Arquivo lido com sucesso. Colunas: {df.columns.tolist()}")
                
                # Análise básica
                results.append(f"\nAnálise do arquivo {file}:")
                results.append(f"- Número de linhas: {len(df)}")
                results.append(f"- Colunas disponíveis: {', '.join(df.columns)}")
                
                # Análise específica baseada na query
                if "frequentes" in query.lower() and "servico" in df.columns:
                    logger.info("Calculando serviços mais frequentes")
                    servicos_freq = df["servico"].value_counts().head(5)
                    results.append("\nServiços mais frequentes:")
                    for servico, count in servicos_freq.items():
                        results.append(f"- {servico}: {count} vezes")

            except Exception as e:
                logger.error(f"Erro ao analisar {file}: {str(e)}")
                results.append(f"Erro ao analisar {file}: {str(e)}")

        logger.info("Análise concluída")
        return "\n".join(results)

    return [
        Tool(
            name="analyze_data",
            func=analyze_data,
            description="Analisa os dados com base em uma query específica. Use para buscar informações sobre notas fiscais, valores, datas, etc."
        )
    ] 