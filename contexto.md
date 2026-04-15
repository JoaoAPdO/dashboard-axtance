# 📊 Projeto: Dashboard e Diagnóstico de Risco Ocupacional (Axtance)

## 🎯 Objetivo Geral
Criar um sistema automatizado que extrai dados de uma pesquisa de Clima e Risco Ocupacional do Google Sheets, exibe uma Dashboard interativa em tempo real e utiliza IA para gerar diagnósticos empresariais detalhados.

## 🛠️ Stack Tecnológica
* **Linguagem:** Python 3
* **Ambiente:** Virtual Environment (`.venv`)
* **Extração de Dados:** `gspread`, API Google Sheets, API Google Drive
* **Manipulação de Dados:** `pandas`
* **Front-end / Visualização:** `streamlit`

## 📁 Estrutura de Arquivos
1.  `credentials.json` (ARQUIVO SENSÍVEL - Ignorado no Git): Chaves da Conta de Serviço do Google Cloud.
2.  `conexao.py`: Gerencia a autenticação com as APIs do Google.
3.  `dados.py`: Faz o download da planilha, força a leitura das colunas (tratando nomes duplicados) e retorna um DataFrame do Pandas.
4.  `dashboard.py`: Arquivo principal da interface de usuário. Arquitetado em funções (Clean Code), contendo sistema de cache, abas de navegação, gráficos interativos e filtragem determinística de perguntas abertas.

## 📌 Status Atual (Fases Concluídas)
* [x] **Fase 1:** Conexão com Google Cloud estabelecida.
* [x] **Fase 2:** Tratamento de dados "crus" para DataFrame funcional.
* [x] **Fase 3:** Dashboard em Streamlit refatorado, modularizado, com cache ativo e filtros limpos (sem erros de renderização gráfica).

## 🚀 Próximos Passos (Backlog)
* **Fase 4 (Deployment - Ponto 4):** Tirar a Dashboard do ambiente local (VS Code) e publicá-la (hospedagem) para acesso de usuários leigos via link web.
* **Fase 5 (Integração de IA):** Conectar o sistema local a uma API de Inteligência Artificial.
* **Fase 6 (Engenharia de Prompt):** Criar a lógica para ler a tabela gerada no `dados.py` e cuspir um diagnóstico automatizado baseado nos resultados da pesquisa.

## ⚠️ Regras de Negócio Importantes
1.  O sistema gráfico do Streamlit (Altair) não suporta caracteres como `:` nos nomes dos eixos X/Y. Os dados sempre devem ser limpos com `.reset_index()` antes da renderização de gráficos.
2.  Novas perguntas de texto livre adicionadas na pesquisa devem ter seu nome exato inserido na lista `PERGUNTAS_ABERTAS` no arquivo `dashboard.py` para não gerarem gráficos quebrados.