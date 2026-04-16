# 📊 Projeto: Dashboard e Diagnóstico de Risco Ocupacional (Axtance)

## 🎯 Objetivo Geral
Criar um sistema automatizado que extrai dados de uma pesquisa de Clima e Risco Ocupacional do Google Sheets, exibe uma Dashboard interativa em tempo real e utiliza IA para gerar diagnósticos empresariais detalhados e planos de ação estratégicos.

## 🛠️ Stack Tecnológica
* **Linguagem:** Python 3.10+
* **Ambiente:** Virtual Environment (`.venv`)
* **Extração de Dados:** `gspread`, API Google Sheets, API Google Drive
* **Manipulação de Dados:** `pandas`
* **Front-end / Visualização e Hospedagem:** `streamlit`, Streamlit Community Cloud
* **Inteligência Artificial:** `google-genai` (Google Gemini API - Modelo `gemini-3-flash-preview` integrado com configurações avançadas de tipo)
* **Segurança:** `python-dotenv` (Gestão de variáveis de ambiente local) e `st.secrets` (Nuvem)

## 📁 Estrutura de Arquivos
1.  `.gitignore`: Bloqueia o envio de credenciais e arquivos temporários para o repositório público.
2.  `requirements.txt`: Lista de dependências para o servidor da nuvem (Streamlit). *Sempre manter atualizado ao atualizar pacotes vitais como `google-genai`.*
3.  `credentials.json` (SENSÍVEL - Ignorado no Git): Chaves da Conta de Serviço do GCP (Ambiente Local).
4.  `.env` (SENSÍVEL - Ignorado no Git): Armazena a chave da API do Gemini sem aspas (Ambiente Local).
5.  `conexao.py`: Gerencia a autenticação com o Google Sheets, otimizado com `@st.cache_resource`.
6.  `dados.py`: Faz o download da planilha, trata colunas e retorna um DataFrame (`@st.cache_data`).
7.  `dashboard.py`: Interface principal do usuário (Clean Code). Organizada em 4 abas (Visão Geral, Análise Detalhada, Dados Crus e Diagnóstico IA), com proteção contra erros de renderização.
8.  `ia_engine.py`: Motor de IA isolado. Transforma os dados em texto estruturado neutro e aplica engenharia de prompt avançada (System Instructions + Controle de Temperatura) para gerar diagnósticos via Gemini.

## 📌 Status Atual (Fases Concluídas)
* [x] **Fase 1:** Conexão com Google Cloud estabelecida.
* [x] **Fase 2:** Tratamento de dados "crus" para DataFrame funcional.
* [x] **Fase 3:** Dashboard em Streamlit refatorada, com cache ativo e performance otimizada.
* [x] **Fase 4 (Deployment):** Aplicação versionada e publicada com sucesso no Streamlit Community Cloud.
* [x] **Fase 5 (Integração de IA):** Motor de IA construído e funcional.
* [x] **Fase 6 (A Ponte Final):** Tratamento de falhas do Pandas adicionado e Segurança Híbrida implementada.
* [x] **Fase 7 (Migração Gemini 3.0 e Otimização Lógica):** * Atualização do pacote `google-genai` e migração do modelo para `gemini-3-flash-preview`.
    * Implementação da classe `types.GenerateContentConfig` para separação de `system_instruction` e controle de alucinação (`temperature=0.3`).
    * **Correção Crítica de Bug de Contexto:** Remoção de rótulos pré-julgados no Python ("Pontos Críticos") e delegação da interpretação lógica da Escala Likert para as System Instructions da IA.

## 🚀 Próximos Passos (Backlog Futuro)
* [ ] **Exportação de Relatórios:** Implementar funcionalidade para exportar o diagnóstico gerado em PDF para apresentações gerenciais.
* [ ] **Monitoramento de Custos/Tokens:** Avaliar o consumo do novo modelo 3.0 em produção conforme a base de respondentes aumenta.

## ⚠️ Regras de Negócio e Aprendizados Importantes
1.  **Nomenclatura Oficial de API (Gemini 3.0):** Modelos em preview ou mais recentes do Google podem ter nomes diferentes do marketing. O modelo "Gemini 3.0 Flash" deve ser chamado no código obrigatoriamente como `gemini-3-flash-preview` para evitar o erro `404 NOT_FOUND`.
2.  **Neutralidade do Contexto Python:** O Python **não deve** pré-julgar os dados (ex: chamar notas baixas de "Riscos"). Como a pesquisa usa Escala Likert onde 1="Nunca", tirar nota 1.0 em "Dores nas Costas" é excelente. O Python deve enviar dados com rótulos neutros ("Menores Médias").
3.  **Regra Crucial de Interpretação (Prompt):** O motor de IA (`ia_engine.py`) deve sempre conter nas suas *System Instructions* a regra de como interpretar a escala do formulário, ensinando a IA a usar seu raciocínio lógico para deduzir se uma média alta ou baixa é positiva ou negativa dependendo da pergunta.
4.  **Gráficos Altair:** O sistema não suporta caracteres como `:` nos nomes dos eixos. Os dados sempre devem ser limpos com `.reset_index()`.
5.  **Perguntas Abertas:** Novas perguntas de texto livre adicionadas na pesquisa devem ter seu nome exato inserido na lista `PERGUNTAS_ABERTAS`.
6.  **Segurança Híbrida:** O acesso às chaves varia conforme o ambiente:
    * **Local:** Lê de `.env` (sem aspas).
    * **Nuvem (Streamlit Cloud):** Lê de `st.secrets` no formato TOML (com aspas duplas).