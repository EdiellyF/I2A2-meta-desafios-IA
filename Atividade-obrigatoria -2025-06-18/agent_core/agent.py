import os
import logging
from typing import List, Callable
from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import pandas as pd

# Importar as novas ferramentas
from agent_core.tools.consistency_validation import validate_nfe_consistency
from agent_core.tools.item_analysis import (
    list_top_expensive_items,
    list_product_ncm_pairs,
    top_products_by_total_quantity,
    total_value_by_ncm_code,
    avg_item_quantity,
    find_zero_unit_value_items,
    avg_item_total_value,
    find_negative_quantity_items,
    find_inconsistent_item_values
)
from agent_core.tools.header_analysis import (
    analyze_top_emitters_by_value,
    count_notes_by_uf_emitter,
    avg_note_value_by_municipio_emitter,
    list_notes_by_cnpj_emitter,
    analyze_top_recipients_by_value,
    count_notes_by_uf_recipient,
    count_notes_by_municipio_recipient,
    total_value_by_month,
    count_notes_by_specific_date,
    day_of_week_highest_emission,
    count_notes_by_natureza_operacao,
    total_value_by_natureza_operacao,
    find_negative_value_notes,
    find_duplicate_note_numbers
)

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

NFE_AGENT_PROMPT = """Responda *sempre* e *exclusivamente* em português brasileiro.\n\nVocê é um agente especialista em Notas Fiscais Eletrônicas (NF-e) com amplo conhecimento técnico, fiscal e normativo. Seu objetivo é analisar e validar dados fiscais contidos em dois datasets fornecidos: o dataset \"Cabecalhos\", que contém informações principais de cada nota fiscal, incluindo a Chave de Acesso (chave primária e identificador único da nota), Número da Nota, Data de Emissão, Valor Total da Nota e demais campos fiscais; e o dataset \"Itens\", que contém os itens individuais de cada nota fiscal, com informações de Chave de Acesso (chave primária, correspondendo à chave no dataset Cabecalhos), Código do Item, Descrição do Produto, Quantidade, Valor Unitário, Valor Total do Item e demais campos de detalhe.\n\nSua principal tarefa é realizar a validação de consistência entre os dois datasets: para cada Chave de Acesso, você deve verificar se a soma do campo Valor Total do Item de todos os itens associados corresponde exatamente ao Valor Total da Nota no dataset Cabecalhos. Sempre que encontrar divergências, apresente um relatório informando a Chave de Acesso, o Valor Total informado na Nota, a soma calculada dos itens e a diferença apurada.\n\nAlém disso, você deve ser capaz de responder perguntas analíticas e descritivas sobre os dados dos datasets, como: quantidade total de notas fiscais, soma total de valores de notas, número de itens em determinada nota, identificação das maiores notas fiscais emitidas e listagem dos produtos mais comuns. Sempre que possível, apresente as respostas em forma de tabela, lista ou resumo numérico, conforme for mais adequado.\n\nVocê também deve identificar anomalias fiscais, como notas fiscais com valor total zerado, notas fiscais sem itens associados, e itens com valores unitários nulos ou negativos. Suas respostas devem ser técnicas, claras, objetivas e fundamentadas. Sempre explique o raciocínio seguido ao apresentar suas conclusões. Utilize a Chave de Acesso como chave primária para todas as operações de cruzamento de dados. Em caso de ausência de dados ou limitações nos arquivos fornecidos, informe a limitação de forma transparente e prossiga com a análise possível.\n\nVocê tem acesso às seguintes ferramentas:\n\n{tools}\n\nUse o seguinte formato:\n\nQuestion: a pergunta que você precisa responder\nThought: você deve sempre pensar sobre o que fazer\nAction: a ação a ser tomada, deve ser uma das [{tool_names}]\nAction Input: o input para a ação\nObservation: o resultado da ação\n... (este Thought/Action/Action Input/Observation pode se repetir N vezes)\nThought: agora eu sei a resposta final\nFinal Answer: a resposta final para a pergunta original (em português brasileiro)"""

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
        
        # Define as ferramentas para análise dos dados
        tools = [
            Tool(
                name="analisar_cabecalhos",
                func=lambda x: f"Análise do cabeçalho: Total de notas: {len(cabecalho_df)}, Valor total: R$ {cabecalho_df['VALOR NOTA FISCAL'].sum():,.2f}",
                description="Analisa os dados do cabeçalho das notas fiscais, fornecendo um resumo geral."
            ),
            Tool(
                name="analisar_itens",
                func=lambda x: f"Análise dos itens: Total de itens: {len(itens_df)}, Serviços únicos: {itens_df['DESCRIÇÃO DO PRODUTO/SERVIÇO'].nunique()}",
                description="Analisa os dados dos itens das notas fiscais, fornecendo um resumo geral."
            ),
            Tool(
                name="validar_consistencia",
                func=lambda x: validate_nfe_consistency(cabecalho_df, itens_df),
                description="Valida a consistência entre os valores do cabeçalho e dos itens. Retorna um relatório detalhado de divergências (Chave de Acesso, Valor Total da Nota, Soma dos Itens, Diferença) ou confirma a consistência."
            ),
            Tool(
                name="listar_top_produtos_caros",
                func=lambda x: list_top_expensive_items(itens_df, 10),
                description="Lista os 10 produtos/serviços mais caros encontrados nos dados dos itens, com base no valor unitário. Ideal para perguntas sobre os itens de maior valor."
            ),
            Tool(
                name="listar_descricoes_ncm",
                func=lambda x: list_product_ncm_pairs(itens_df),
                description="Lista todas as descrições únicas de produtos/serviços e seus respectivos códigos NCM/SH encontrados nos dados dos itens. Útil para entender a variedade de produtos e suas classificações fiscais."
            ),
            Tool(
                name="analisar_top_emitentes_por_valor",
                func=lambda x: analyze_top_emitters_by_value(cabecalho_df),
                description="Analisa e lista as 5 Razões Sociais Emitentes com o maior valor total de notas fiscais emitidas."
            ),
            Tool(
                name="contar_notas_por_uf_emitente",
                func=lambda x: count_notes_by_uf_emitter(cabecalho_df),
                description="Conta o número de notas fiscais registradas por cada UF Emitente."
            ),
            Tool(
                name="valor_medio_por_municipio_emitente",
                func=lambda x: avg_note_value_by_municipio_emitter(cabecalho_df),
                description="Calcula e lista o valor médio das notas fiscais por cada Município Emitente."
            ),
            Tool(
                name="listar_notas_por_cnpj_emitente",
                func=lambda cnpj: list_notes_by_cnpj_emitter(cabecalho_df, cnpj),
                description="Lista as notas fiscais emitidas por um CPF/CNPJ Emitente específico. O input deve ser o CNPJ como string."
            ),
            Tool(
                name="analisar_top_destinatarios_por_valor",
                func=lambda x: analyze_top_recipients_by_value(cabecalho_df),
                description="Analisa e lista os 5 Nomes de Destinatários que receberam o maior valor total de notas fiscais."
            ),
            Tool(
                name="contar_notas_por_uf_destinatario",
                func=lambda x: count_notes_by_uf_recipient(cabecalho_df),
                description="Conta o número de notas fiscais recebidas por cada UF Destinatário."
            ),
            Tool(
                name="contar_notas_por_municipio_destinatario",
                func=lambda x: count_notes_by_municipio_recipient(cabecalho_df),
                description="Conta o número de notas fiscais recebidas por cada Município Destinatário."
            ),
            Tool(
                name="valor_total_por_mes",
                func=lambda x: total_value_by_month(cabecalho_df),
                description="Calcula o valor total das notas fiscais por mês de emissão."
            ),
            Tool(
                name="contar_notas_por_data_especifica",
                func=lambda date_str: count_notes_by_specific_date(cabecalho_df, date_str),
                description="Conta o número de notas fiscais emitidas em uma data específica. O input deve ser a data no formato 'YYYY-MM-DD'."
            ),
            Tool(
                name="dia_semana_maior_emissao",
                func=lambda x: day_of_week_highest_emission(cabecalho_df),
                description="Identifica o dia da semana com o maior número de emissões de notas fiscais."
            ),
            Tool(
                name="contar_notas_por_natureza_operacao",
                func=lambda x: count_notes_by_natureza_operacao(cabecalho_df),
                description="Conta o número de notas fiscais para cada tipo de Natureza da Operação."
            ),
            Tool(
                name="valor_total_por_natureza_operacao",
                func=lambda natureza: total_value_by_natureza_operacao(cabecalho_df, natureza),
                description="Calcula o valor total das notas fiscais para uma Natureza da Operação específica. O input deve ser parte do nome da natureza da operação como string."
            ),
            Tool(
                name="encontrar_notas_valor_negativo",
                func=lambda x: find_negative_value_notes(cabecalho_df),
                description="Identifica e lista notas fiscais no cabeçalho com VALOR NOTA FISCAL negativo."
            ),
            Tool(
                name="encontrar_numeros_nota_duplicados",
                func=lambda x: find_duplicate_note_numbers(cabecalho_df),
                description="Identifica e lista notas fiscais com NÚMERO duplicado."
            ),
            Tool(
                name="top_produtos_por_quantidade_total",
                func=lambda x: top_products_by_total_quantity(itens_df),
                description="Identifica e lista os 10 produtos/serviços com a maior QUANTIDADE total acumulada."
            ),
            Tool(
                name="valor_total_por_codigo_ncm",
                func=lambda ncm: total_value_by_ncm_code(itens_df, ncm),
                description="Calcula o valor total de todos os itens para um CÓDIGO NCM/SH específico. O input deve ser o código NCM como string."
            ),
            Tool(
                name="quantidade_media_por_item",
                func=lambda x: avg_item_quantity(itens_df),
                description="Calcula a QUANTIDADE média por item em todas as notas."
            ),
            Tool(
                name="encontrar_itens_valor_unitario_zerado",
                func=lambda x: find_zero_unit_value_items(itens_df),
                description="Identifica e lista itens com VALOR UNITÁRIO zerado."
            ),
            Tool(
                name="valor_total_medio_de_item",
                func=lambda x: avg_item_total_value(itens_df),
                description="Calcula o VALOR TOTAL médio de um item."
            ),
            Tool(
                name="encontrar_itens_quantidade_negativa",
                func=lambda x: find_negative_quantity_items(itens_df),
                description="Identifica e lista itens com QUANTIDADE negativa."
            ),
            Tool(
                name="encontrar_inconsistencias_valor_item",
                func=lambda x: find_inconsistent_item_values(itens_df),
                description="Identifica e lista itens onde o VALOR TOTAL não é igual a (QUANTIDADE * VALOR UNITÁRIO)."
            ),
            Tool(
                name="identificar_anomalias",
                func=lambda x: "Identificação de anomalias fiscais", 
                description="Identifica anomalias fiscais nos dados (placeholder, pode ser expandida para usar as novas ferramentas de anomalia)."
            )
        ]
        
        # Cria e executa o agente
        logger.info("Criando agente NFe")
        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )
        
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
        
        # Executa o agente
        logger.info("Executando agente NFe")
        response = agent.run(context)
        logger.info("Agente finalizado com sucesso")
        logger.info(f"Resposta do agente: {response}")
        
        return response
        
    except Exception as e:
        logger.error(f"Erro na execução do agente: {str(e)}")
        return f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}" 