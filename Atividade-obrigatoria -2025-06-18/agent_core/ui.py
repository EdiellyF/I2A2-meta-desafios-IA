import streamlit as st
from agent_core.utils import extract_zip, find_data_files
from agent_core.agent import run_agent_with_middlewares
import os
import shutil

def render_chat_interface():
    st.markdown("""
        <style>
        .stChatMessage.user {background: #f0f4fa; border-radius: 12px; margin-bottom: 8px; padding: 10px;}
        .stChatMessage.agent {background: #e6f7e6; border-radius: 12px; margin-bottom: 8px; padding: 10px;}
        .stChatInput {margin-top: 0.5rem;}
        </style>
    """, unsafe_allow_html=True)

    st.title("🔍 Analisador Autônomo de Dados - Chat")
    st.caption("Faça perguntas sobre seus arquivos de dados (CSV/Excel em ZIP) de forma conversacional!")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'temp_dir' not in st.session_state:
        st.session_state.temp_dir = None

    with st.sidebar:
        uploaded_file = st.file_uploader("Carregue arquivo ZIP", type=["zip"])
        if uploaded_file:
            temp_zip_path = "temp_zip.zip"
            with open(temp_zip_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            temp_dir = extract_zip(temp_zip_path)
            st.session_state.uploaded_file = uploaded_file
            st.session_state.temp_dir = temp_dir
            st.success("Arquivo carregado!")
            if os.path.exists(temp_zip_path):
                os.remove(temp_zip_path)
        if st.session_state.temp_dir:
            files = find_data_files(st.session_state.temp_dir)
            st.markdown("**Arquivos extraídos:**")
            for f in files:
                st.markdown(f"- {f}")

    st.divider()
    st.markdown("### Chat com o agente")
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"<div class='stChatMessage user'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='stChatMessage agent'><b>Agente:</b> {msg['content']}</div>", unsafe_allow_html=True)

    if st.session_state.temp_dir:
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Digite sua pergunta:", key="chat_input", placeholder="Ex: Quais notas fiscais têm valor acima de R$ 10.000?")
            submit = st.form_submit_button("Enviar")
        if submit and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("Processando resposta..."):
                try:
                    response = run_agent_with_middlewares(user_input, st.session_state.temp_dir, find_data_files)
                    st.session_state.chat_history.append({"role": "agent", "content": response})
                    st.experimental_rerun()
                except Exception as e:
                    st.session_state.chat_history.append({"role": "agent", "content": f"Erro: {e}"})
                    st.experimental_rerun()
    else:
        st.info("Faça upload de um arquivo ZIP na barra lateral para começar a conversar com o agente.")

    # Limpeza do diretório temporário ao final da sessão
    if st.button("Limpar histórico e arquivos", type="primary"):
        st.session_state.chat_history = []
        if st.session_state.temp_dir and os.path.exists(st.session_state.temp_dir):
            shutil.rmtree(st.session_state.temp_dir)
        st.session_state.temp_dir = None
        st.session_state.uploaded_file = None
        st.success("Histórico e arquivos limpos!") 