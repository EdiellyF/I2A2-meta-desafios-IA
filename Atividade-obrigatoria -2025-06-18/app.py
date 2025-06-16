import streamlit as st
import os
import tempfile
import zipfile
import pandas as pd
from agent_core.agent import run_agent_with_middlewares
import logging

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def find_data_files(temp_dir: str) -> list:
    """Lista todos os arquivos de dados no diretório temporário."""
    logger.info(f"Procurando arquivos em: {temp_dir}")
    files = []
    for file in os.listdir(temp_dir):
        if file.endswith(('.csv', '.xlsx', '.xls')):
            files.append(file)
    logger.info(f"Arquivos encontrados: {files}")
    return files

def main():
    st.title("📊 Análise de Notas Fiscais")
    
    # Upload do arquivo ZIP
    uploaded_file = st.file_uploader("Faça upload do arquivo ZIP com as notas fiscais", type=['zip'])
    
    if uploaded_file is not None:
        # Cria diretório temporário
        with tempfile.TemporaryDirectory() as temp_dir:
            # Salva o arquivo ZIP
            zip_path = os.path.join(temp_dir, "notas.zip")
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Extrai o ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Lista os arquivos extraídos
            files = find_data_files(temp_dir)
            if files:
                st.success(f"✅ {len(files)} arquivos encontrados!")
                st.write("Arquivos disponíveis:")
                for file in files:
                    st.write(f"- {file}")
                
                # Interface de perguntas
                st.subheader("💭 Faça sua pergunta")
                question = st.text_input("Digite sua pergunta sobre os dados:")
                
                if question:
                    try:
                        # Processa a pergunta
                        with st.spinner("Processando sua pergunta..."):
                            response = run_agent_with_middlewares(question, temp_dir, find_data_files)
                            st.write("Resposta:")
                            st.write(response)
                    except Exception as e:
                        st.error(f"Erro ao processar pergunta: {str(e)}")
            else:
                st.error("❌ Nenhum arquivo de dados encontrado no ZIP!")

if __name__ == "__main__":
    main() 