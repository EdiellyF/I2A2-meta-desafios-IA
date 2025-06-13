import streamlit as st
from agent_core.utils import save_uploaded_zip, extract_zip, find_data_files
from agent_core.agent import run_agent_with_middlewares

def render_chat_interface():
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
            .stApp {
                color: #FFFFFF;
                background-color: #000000;
            }
            .stText, .stMarkdown, .stTitle, .stSubheader, .stWrite {
                color: #FFFFFF;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("📊 Análise de Notas Fiscais")
    st.empty()  
    uploaded_file = st.file_uploader("Faça upload do arquivo ZIP com as notas fiscais", type=['zip'])
    if uploaded_file:
        # Salva o arquivo enviado e obtém o diretório temporário e caminho do ZIP salvo.
        temp_dir, zip_path = save_uploaded_zip(uploaded_file)
        # Extrai o ZIP para o mesmo diretório
        extract_zip(zip_path)
        files = find_data_files(temp_dir)
        if files:
            st.success(f"✅ {len(files)} arquivos encontrados!")
            st.write("Arquivos disponíveis:")
            for file in files:
                st.write(f"- {file}")
            st.subheader("💭 Faça sua pergunta")
            question = st.text_input("Digite sua pergunta sobre os dados:")
            if question:
                try:
                    with st.spinner("Processando sua pergunta..."):
                        response = run_agent_with_middlewares(question, temp_dir, find_data_files)
                        st.write("Resposta:")
                        st.write(response)
                except Exception as e:
                    st.error(f"Erro ao processar pergunta: {str(e)}")
        else:
            st.error("❌ Nenhum arquivo de dados encontrado no ZIP!")
