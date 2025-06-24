import os
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

def get_llm():
    """
    Retorna uma instância do LLM configurada.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")
    
    logger.info("Inicializando ChatGoogleGenerativeAI...")
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        logger.info("ChatGoogleGenerativeAI inicializado com sucesso!")
        return llm
    except Exception as e:
        logger.error(f"Erro ao inicializar ChatGoogleGenerativeAI: {str(e)}")
        raise
    # Adicione outros provedores aqui (OpenAI, VertexAI, etc)
    raise ValueError("LLM provider não suportado ou não configurado.") 