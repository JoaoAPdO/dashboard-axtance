# 📊 Projeto: Dashboard e Diagnóstico de Risco Ocupacional (Axtance)

## 🎯 Objetivo Geral
Criar um sistema automatizado que extrai dados de uma pesquisa de Clima e Risco Ocupacional do Google Sheets, exibe uma Dashboard interativa em tempo real e utiliza IA para gerar diagnósticos empresariais detalhados e planos de ação estratégicos.

## 🛠️ Stack Tecnológica
* **Linguagem:** Python 3.10+
* **Ambiente:** Virtual Environment (`.venv`)
* **Extração de Dados:** `gspread`, API Google Sheets, API Google Drive
* **Manipulação de Dados:** `pandas`
* **Front-end / Visualização e Hospedagem:** `streamlit`, Streamlit Community Cloud
* **Inteligência Artificial:** `google-genai` (Google Gemini API - Modelo `gemini-2.5-flash`)
* **Segurança:** `python-dotenv` (Gestão de variáveis de ambiente local) e `st.secrets` (Nuvem)

## 📁 Estrutura de Arquivos
1.  `.gitignore`: Bloqueia o envio de credenciais e arquivos temporários para o repositório público.
2.  `requirements.txt`: Lista de dependências para o servidor da nuvem (Streamlit).
3.  `credentials.json` (SENSÍVEL - Ignorado no Git): Chaves da Conta de Serviço do GCP (Ambiente Local).
4.  `.env` (SENSÍVEL - Ignorado no Git): Armazena a chave da API do Gemini sem aspas (Ambiente Local).
5.  `conexao.py`: Gerencia a autenticação com o Google Sheets, otimizado com `@st.cache_resource`.
6.  `dados.py`: Faz o download da planilha, trata colunas e retorna um DataFrame (`@st.cache_data`).
7.  `dashboard.py`: Interface principal do usuário (Clean Code). Agora organizada em 4 abas (Visão Geral, Análise Detalhada, Dados Crus e Diagnóstico IA), com proteção contra erros de renderização.
8.  `ia_engine.py`: Motor de IA isolado. Transforma os dados em texto estruturado, tenta converter "strings" em números para cálculos precisos, e aplica engenharia de prompt para gerar diagnósticos via Gemini.

## 📌 Status Atual (Fases Concluídas)
* [x] **Fase 1:** Conexão com Google Cloud estabelecida.
* [x] **Fase 2:** Tratamento de dados "crus" para DataFrame funcional.
* [x] **Fase 3:** Dashboard em Streamlit refatorada, com cache ativo e performance otimizada.
* [x] **Fase 4 (Deployment):** Aplicação versionada e publicada com sucesso no Streamlit Community Cloud.
* [x] **Fase 5 (Integração de IA):** Motor de IA construído (`ia_engine.py`) atualizado para o SDK oficial `google-genai`.
* [x] **Fase 6 (A Ponte Final - Integração Concluída):**
    * Criada a função `preparar_contexto_ia` que traduz o DataFrame para texto sem sobrecarregar a dashboard.
    * Tratamento de falhas do Pandas adicionado: conversão forçada de textos para números e processamento de perguntas categóricas por moda (respostas mais frequentes).
    * Aba de Inteligência Artificial implementada e integrada no `dashboard.py`.
    * Segurança Híbrida implementada e testada com sucesso entre o ambiente local e produção.

## 🚀 Próximos Passos (Backlog Futuro)
* [ ] **Exportação de Relatórios:** Implementar funcionalidade para exportar o diagnóstico gerado em PDF para apresentações gerenciais.
* [ ] **Ajuste de Prompts:** Calibrar o nível de rigor do "Consultor Sênior" dependendo das necessidades específicas que surgirem.

## ⚠️ Regras de Negócio Importantes
1.  **Gráficos:** O sistema Altair não suporta caracteres como `:` nos nomes dos eixos. Os dados sempre devem ser limpos com `.reset_index()` antes da renderização de gráficos.
2.  **Perguntas Abertas:** Novas perguntas de texto livre adicionadas na pesquisa devem ter seu nome exato inserido na lista `PERGUNTAS_ABERTAS` no arquivo `dashboard.py`.
3.  **Segurança Híbrida:** O acesso às chaves varia conforme o ambiente:
    * **Local:** Lê de `.env` (ex: `GEMINI_API_KEY=AIzaSy...` -> **sem aspas**).
    * **Nuvem (Streamlit Cloud):** Lê de `st.secrets` no formato TOML (ex: `GEMINI_API_KEY = "AIzaSy..."` -> **com aspas duplas**).
4.  **Tratamento de Dados da IA:** Para contornar como o Google Sheets envia dados, o motor de IA usa `pd.to_numeric` automaticamente em todas as colunas que não sejam abertas, prevenindo o erro "Nenhuma coluna de notas encontrada".
