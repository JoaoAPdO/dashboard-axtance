# 📊 Projeto: Dashboard e Diagnóstico de Risco Ocupacional (Axtance)

## 🎯 Objetivo Geral
Criar um sistema automatizado que extrai dados de uma pesquisa de Clima e Risco Ocupacional do Google Sheets, exibe uma Dashboard interativa em tempo real e utiliza IA para gerar diagnósticos empresariais detalhados.

## 🛠️ Stack Tecnológica
* **Linguagem:** Python 3
* **Ambiente:** Virtual Environment (`.venv`)
* **Extração de Dados:** `gspread`, API Google Sheets, API Google Drive
* **Manipulação de Dados:** `pandas`
* **Front-end / Visualização e Hospedagem:** `streamlit`, Streamlit Community Cloud
* **Inteligência Artificial:** `google-genai` (Google Gemini API)
* **Segurança:** `python-dotenv` (Gestão de variáveis de ambiente)

## 📁 Estrutura de Arquivos
1.  `.gitignore`: Bloqueia o envio de credenciais e arquivos temporários para o repositório público.
2.  `requirements.txt`: Lista de dependências para o servidor da nuvem (Streamlit).
3.  `credentials.json` (SENSÍVEL - Ignorado no Git): Chaves da Conta de Serviço do GCP (Ambiente Local).
4.  `.env` (SENSÍVEL - Ignorado no Git): Armazena a chave da API do Gemini (Ambiente Local).
5.  `conexao.py`: Gerencia a autenticação com o Google Sheets, buscando localmente (`credentials.json`) ou na nuvem (`st.secrets`), otimizado com `@st.cache_resource`.
6.  `dados.py`: Faz o download da planilha, trata colunas duplicadas e retorna um DataFrame (`@st.cache_data`).
7.  `dashboard.py`: Interface principal do usuário (Clean Code), com abas, gráficos interativos e proteção contra dados nulos.
8.  `ia_engine.py`: Módulo isolado de Inteligência Artificial. Conecta à API do Gemini e aplica engenharia de prompt para gerar diagnósticos.

## 📌 Status Atual (Fases Concluídas)
* [x] **Fase 1:** Conexão com Google Cloud estabelecida.
* [x] **Fase 2:** Tratamento de dados "crus" para DataFrame funcional.
* [x] **Fase 3:** Dashboard em Streamlit refatorada, com cache ativo e performance otimizada (Cold Start minimizado e Hot Reloads instantâneos).
* [x] **Fase 4 (Deployment):** Aplicação versionada via Git/GitHub e publicada com sucesso no Streamlit Community Cloud, com Secrets configurados.
* [x] **Fase 5 (Integração de IA):** Motor de IA construído (`ia_engine.py`), atualizado para o SDK oficial `google-genai` e utilizando o modelo `gemini-2.5-flash`.

## 🚀 Próximos Passos (Backlog)
* **Fase 6 (A Ponte Final - Integração):** 1. Criar uma função para transformar o DataFrame da planilha real em um texto enxuto.
    2. Adicionar uma nova aba ou botão no `dashboard.py` para acionar a IA.
    3. Exibir o diagnóstico gerado diretamente na interface web da Dashboard.
    4. Atualizar a nuvem (Git Push) com as novidades.

## ⚠️ Regras de Negócio Importantes
1.  **Gráficos:** O sistema Altair não suporta caracteres como `:` nos nomes dos eixos X/Y. Os dados sempre devem ser limpos com `.reset_index()` antes da renderização de gráficos de barras.
2.  **Perguntas Abertas:** Novas perguntas de texto livre adicionadas na pesquisa devem ter seu nome exato inserido na lista `PERGUNTAS_ABERTAS` no arquivo `dashboard.py`.
3.  **Segurança Híbrida:** Todos os serviços externos (Google Sheets e Gemini) devem ter duplo tratamento de chaves: buscar no disco local durante o desenvolvimento e em `st.secrets` quando em produção.