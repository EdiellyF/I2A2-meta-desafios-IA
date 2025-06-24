import functools
import logging
from typing import Callable, Any

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_input(question: str) -> str:
    """
    Valida a entrada do usuário.
    """
    if not question or not question.strip():
        raise ValueError("A pergunta não pode estar vazia")
    return question.strip()

def log_agent_execution(func: Callable) -> Any:
    """
    Middleware para logar a execução do agente.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executando agente com pergunta: {kwargs.get('input', args[0] if args else 'N/A')}")
        result = func(*args, **kwargs)
        logger.info(f"Resposta do agente: {result}")
        return result
    return wrapper

def cache_results(func: Callable) -> Any:
    """
    Middleware para cache de resultados.
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in cache:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    return wrapper

def handle_errors(error: Exception) -> str:
    """
    Middleware para tratamento de erros.
    """
    logger.error(f"Erro na execução do agente: {str(error)}")
    return f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(error)}" 