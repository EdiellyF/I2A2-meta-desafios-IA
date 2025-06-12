import os
import logging
from typing import List, Callable
from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import pandas as pd

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

def run_agent_with_middlewares(question: str, temp_dir: str, find_data_files: Callable[[str], List[str]]) -> str:
    """
    Executa o agente com middlewares aplicados.
    """
    logger.info(f"Iniciando processamento da pergunta: {question}")
    
    try:
        # Configura o LLM
        logger.info("Configurando LLM")
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True,
            model_kwargs={"generation_config": {"temperature": 0.7}}
        )
        
        # Carrega os arquivos
        logger.info("Carregando arquivos")
        files = find_data_files(temp_dir)
        if not files:
            return "Nenhum arquivo encontrado para análise."
        
        cabecalho_df = None
        itens_df = None
        
        for file in files:
            try:
                file_path = os.path.join(temp_dir, file)
                logger.info(f"Processando arquivo: {file_path}")
                
                if "Cabecalho" in file:
                    cabecalho_df = pd.read_csv(file_path)
                    logger.info(f"Cabeçalho carregado. Colunas: {cabecalho_df.columns.tolist()}")
                elif "Itens" in file:
                    itens_df = pd.read_csv(file_path)
                    logger.info(f"Itens carregados. Colunas: {itens_df.columns.tolist()}")
                    
            except Exception as e:
                logger.error(f"Erro ao carregar {file}: {str(e)}")
        
        if cabecalho_df is None or itens_df is None:
            return "Não foi possível carregar todos os arquivos necessários."
        
        # Prepara o contexto
        context = f"""
        Dados disponíveis:
        
        Cabeçalho das notas fiscais:
        - Total de notas: {len(cabecalho_df)}
        - Valor total: R$ {cabecalho_df['VALOR NOTA FISCAL'].sum():,.2f}
        - Média por nota: R$ {cabecalho_df['VALOR NOTA FISCAL'].mean():,.2f}
        
        Itens das notas fiscais:
        - Total de itens: {len(itens_df)}
        - Serviços únicos: {itens_df['DESCRIÇÃO DO PRODUTO/SERVIÇO'].nunique()}
        
        Pergunta: {question}
        """
        
        # Executa o LLM diretamente
        logger.info("Executando LLM")
        response = llm.invoke(context)
        logger.info("LLM finalizado com sucesso")
        logger.info(f"Resposta do LLM: {response}")
        
        return response.content
        
    except Exception as e:
        logger.error(f"Erro na execução do agente: {str(e)}")
        return f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}" 