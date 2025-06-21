# Análise de Notas Fiscais com LangChain

Este projeto implementa um agente autônomo para análise de notas fiscais usando LangChain e Google Gemini. O agente é capaz de processar arquivos CSV de notas fiscais e responder perguntas sobre os dados.

## Estrutura do Projeto

```
.
├── app.py                 # Interface Streamlit
├── agent_core/           # Core do agente
│   ├── __init__.py
│   ├── agent.py          # Implementação do agente
│   └── llm_factory.py    # Configuração do LLM
├── requirements.txt      # Dependências
└── README.md            # Este arquivo
```

## Funcionalidades

- Upload de arquivo ZIP contendo notas fiscais
- Extração automática dos arquivos CSV
- Análise de dados usando LangChain e Google Gemini
- Interface amigável com Streamlit
- Respostas em linguagem natural

## Requisitos

- Python 3.8+
- Conta Google Cloud com API Key do Gemini
- Arquivo ZIP contendo notas fiscais no formato especificado

## Instalação

1. Clone o repositório:
```bash
git clone
cd 
```

2. Instale as dependências:
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
   - "Qual é a média de valor por nota fiscal?"
   - "Quais são os 3 fornecedores que mais emitiram notas?"
   - "Quais são as naturezas de operação mais comuns?"
   - "Quais são os 5 fornecedores que mais emitiram notas em valor?"
   - "Quantas notas fiscais foram recebidas por cada UF destinatário?"
   - "Liste todas as descrições de produtos/serviços e seus respectivos NCM."
   - "Existem itens onde o valor total não bate com a multiplicação da quantidade pelo valor unitário?"
   

## Tecnologias Utilizadas

- **LangChain**: Framework para construção de agentes de IA
- **Google Gemini**: Modelo de linguagem para processamento de perguntas
- **Streamlit**: Framework para interface web
- **Pandas**: Biblioteca para manipulação de dados
- **Python-dotenv**: Gerenciamento de variáveis de ambiente

## Estrutura dos Dados

O projeto espera um arquivo ZIP contendo dois arquivos CSV:

1. `202401_NFs_Cabecalho.csv`: Contém informações do cabeçalho das notas fiscais
   - CHAVE DE ACESSO
   - MODELO
   - SÉRIE
   - NÚMERO
   - VALOR NOTA FISCAL
   - RAZÃO SOCIAL EMITENTE
   - etc.

2. `202401_NFs_Itens.csv`: Contém os itens das notas fiscais
   - CHAVE DE ACESSO
   - DESCRIÇÃO DO PRODUTO/SERVIÇO
   - VALOR UNITÁRIO
   - VALOR TOTAL
   - etc.

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
