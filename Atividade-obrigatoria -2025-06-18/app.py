import streamlit as st
from agent_core.ui import render_chat_interface

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    render_chat_interface()
    

if __name__ == "__main__":
    main()