# 📊 Projeto: Dashboard e Diagnóstico de Risco Ocupacional (Axtance)

## 🎯 Objetivo Geral
Criar um sistema automatizado que extrai dados de uma pesquisa de Clima e Risco Ocupacional do Google Sheets, exibe uma Dashboard interativa em tempo real e utiliza IA para gerar diagnósticos empresariais detalhados e planos de ação estratégicos embasados na legislação vigente.

## 🛠️ Stack Tecnológica
* **Linguagem:** Python 3.10+
* **Ambiente:** Virtual Environment (`.venv`)
* **Extração de Dados:** `gspread`, API Google Sheets, API Google Drive
* **Manipulação de Dados:** `pandas`
* **Front-end / Visualização e Hospedagem:** `streamlit`, Streamlit Community Cloud
* **Inteligência Artificial:** `google-genai` (Google Gemini API)
  * **Modelo Atual:** `gemini-2.5-flash` (Versão de produção estável, escolhida para evitar erros de alta demanda '503').
  * **Recursos Avançados:** *File API* (Injeção de documentos locais) e *Streaming* (Resposta em tempo real).
* **Segurança:** `python-dotenv` (Gestão de variáveis de ambiente local) e `st.secrets` (Nuvem)

## 📁 Estrutura de Arquivos
1.  `.gitignore`: Bloqueia o envio de credenciais e arquivos temporários para o repositório público.
2.  `requirements.txt`: Lista de dependências para o servidor da nuvem (Streamlit). Dependência essencial da IA atualizada para `google-genai`.
3.  `credentials.json` (SENSÍVEL - Ignorado no Git): Chaves da Conta de Serviço do GCP (Ambiente Local).
4.  `.env` (SENSÍVEL - Ignorado no Git): Armazena a chave da API do Gemini sem aspas (Ambiente Local).
5.  `conexao.py`: Gerencia a autenticação com o Google Sheets, otimizado com `@st.cache_resource`.
6.  `dados.py`: Faz o download da planilha, trata colunas e retorna um DataFrame (`@st.cache_data`).
7.  `dashboard.py`: Interface principal. Renderiza as abas e consome os dados gerados pela IA via *Stream* (`st.write_stream`).
8.  `ia_engine.py`: Motor de IA. Gerencia o *prompting*, injeção de PDFs e retorna o gerador de texto (Streaming) mantendo a conexão ativa.
9.  `knowledge_manager.py`: [NOVO] Gerenciador da Base de Conhecimento. Lê os PDFs e faz upload para a File API do Gemini mantendo-os em cache.
10. `base_conhecimento/`: [NOVO] Diretório físico contendo os PDFs das Normas Regulamentadoras (NRs) e cartilhas oficiais sem acentos no nome.

## 📌 Status Atual (Fases Concluídas)
* [x] **Fase 1 a 4:** Conexão Google Cloud, Tratamento Pandas, Dashboard Streamlit e Deploy em Nuvem.
* [x] **Fase 5 a 7:** Motor de IA com System Instructions avançadas, Neutralidade de Contexto e Segurança Híbrida.
* [x] **Fase 8 (Base de Conhecimento e Compliance):** Implementação da File API do Gemini. A IA agora atua como auditora, lendo Normas Regulamentadoras (NRs) em PDF e citando artigos oficiais no diagnóstico. Otimização de cache com `ttl="47h"` para evitar uploads redundantes e economizar tokens.
* [x] **Fase 9 (Arquitetura de Streaming e Estabilidade):** * Migração para o modelo `gemini-2.5-flash` para garantir 100% de *uptime* e evitar erros 503 (Alta demanda).
    * Implementação de respostas em *Streaming* (fluxo contínuo) usando `yield` para contornar o limite de *Timeout* (Erro 504) imposto pela leitura de múltiplos PDFs simultâneos.

## 🚀 Próximos Passos (Backlog Futuro)
* [ ] **Exportação de Relatórios (PDF):** Implementar funcionalidade (ex: via biblioteca `fpdf2`) para exportar o diagnóstico gerado na tela em um documento PDF bem formatado para apresentações gerenciais.
* [ ] **Gestão Dinâmica da Base de Conhecimento:** Criar uma interface no Streamlit (aba de configurações) para o usuário RH fazer upload de regimentos internos temporários da empresa para a IA cruzar com as NRs.

## ⚠️ Regras de Negócio e Aprendizados Importantes
1.  **Segurança Híbrida:** O acesso às chaves varia: Local lê de `.env` (sem aspas); Nuvem lê de `st.secrets` no formato TOML (com aspas duplas). Lógica com `try...except` é obrigatória para evitar quebra em testes locais.
2.  **Neutralidade e Interpretação (Escala Likert):** O Python envia dados neutros. As *System Instructions* ensinam a IA a deduzir que nota 1.0 em "Dores" é um Ponto Forte, delegando a inteligência lógica ao modelo.
3.  **File API e Nomenclatura (ASCII Codec):** Os arquivos na pasta `base_conhecimento/` **não podem ter acentos, cedilhas ou espaços**. Ex: usar `manual-nr-01.pdf`. Acentos quebram o envio para a API do Google.
4.  **Display Name no Upload:** Ao usar a File API do novo SDK, é obrigatório declarar `config={"display_name": pdf_path.name}`, caso contrário o arquivo sobe, mas o nome retorna como `None` na Dashboard.
5.  **Escopo do Cache do Streamlit (`@st.cache_resource`):** A inicialização do `client = genai.Client()` deve ocorrer **dentro** da função cacheada que faz o upload dos PDFs. Variáveis globais fora da função são esquecidas pelo ambiente isolado do cache, gerando `name 'client' is not defined`.
6.  **Erro 504 (Timeout) e Streaming:** O Gemini processa centenas de páginas, mas a conexão cai após 60 segundos de silêncio. Para contornar, o método de envio deve ser `generate_content_stream`.
7.  **Gerenciamento de Memória (Client Closed):** Em arquiteturas de *Streaming*, a função que aciona a API deve usar a palavra-chave nativa `yield` num loop `for chunk in response_stream: yield chunk.text`. Se você tentar retornar uma subfunção geradora, o Python encerra a função principal, a ferramenta de "Garbage Collection" fecha a conexão do `client`, e o Streamlit devolve o erro: `Cannot send a request, as the client has been closed`.
8.  **TTL do Cache:** Documentos enviados via File API expiram no Google em 48h. A função de upload no Streamlit deve usar `@st.cache_resource(ttl="47h")` para forçar uma renovação automática 1 hora antes de expirar.
