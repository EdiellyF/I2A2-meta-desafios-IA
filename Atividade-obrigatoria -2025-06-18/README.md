# Análise de Notas Fiscais com LangChain

Este projeto implementa um agente autônomo para análise de notas fiscais usando LangChain e Google Gemini. O agente é capaz de processar arquivos CSV de notas fiscais e responder perguntas sobre os dados.

## Estrutura do Projeto

```
├── app.py                       # Ponto de entrada da aplicação
├── services/
│   └── file_service.py          # Funções para upload, extração e listagem de arquivos do ZIP
└── agent_core/
    ├── agent.py                 # Lógica do agente: processamento dos dados e integração com LLM
    ├── ui.py                    # Interface do usuário (Streamlit)
    ├── middlewares.py           # Middlewares (ex.: validação, cache)
    └── utils.py                 # Funções auxiliares e utilitários
```

## Funcionalidades


- **Upload e Extração**: Permite o upload de um arquivo ZIP contendo os dados das notas fiscais, que é automaticamente extraído.
- **Análise de Dados**: Identifica e processa arquivos CSV, XLSX e XLS para extrair informações como total de notas, valor total e média.
- **Consulta Interativa**: Usuário faz perguntas sobre os dados e o agente responde utilizando um LLM.
- **Middlewares**: Implementa middlewares para:
- Validação de perguntas (garante que são suficientemente informativas).
- Cache de resultados para otimizar execuções repetitivas.
- Tratamento de erros.


## Requisitos

- Python 3.8+
- Conta Google Cloud com API Key do Gemini
- Arquivo ZIP contendo notas fiscais no formato especificado

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure a variável de ambiente:
```bash
# Crie um arquivo .env na raiz do projeto
GOOGLE_API_KEY=sua_chave_api_aqui
```

## Uso

1. Inicie a aplicação:
```bash
streamlit run app.py
```

2. Acesse a interface no navegador (geralmente em http://localhost:8501)

3. Faça upload do arquivo ZIP contendo as notas fiscais

4. Faça suas perguntas, por exemplo:
   - "Qual é o valor total das notas fiscais?"
   - "Liste os 5 serviços mais frequentes"
   - "Qual é a média de valor por nota fiscal?"
   - "Quais são os 3 fornecedores que mais emitiram notas?"

## Tecnologias Utilizadas

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [langchain_google_genai](https://github.com/google/langchain_google_genai)
- [Pandas](https://pandas.pydata.org/)
- Outras dependências listadas no `requirements.txt`


## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
