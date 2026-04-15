import os
import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

@st.cache_resource(show_spinner=False)
def inicializar_conexao():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    if os.path.exists('credentials.json'):
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    
    else:
        try:
            creds_dict = dict(st.secrets["gcp_service_account"])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        except Exception as e:
            st.error("Erro estrutural ao carregar credenciais. Verifique os Secrets.")
            raise e

    client = gspread.authorize(creds)
    nome_da_planilha = "INVENTÁRIO DE RISCO OCUPACIONAL (Respostas)"

    try:
        spreadsheet = client.open(nome_da_planilha)
        aba = spreadsheet.get_worksheet(0)
        return aba
    except Exception as e:
        st.error(f"❌ Erro ao tentar abrir a planilha: {e}")
        return None

if __name__ == "__main__":
    print("Iniciando teste de conexão...")
    aba_teste = inicializar_conexao()
    if aba_teste:
        cabecalhos = aba_teste.row_values(1)
        print("✅ Conexão bem-sucedida!")
        print(f"📊 Colunas encontradas: {cabecalhos}")