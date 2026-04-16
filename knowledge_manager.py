import os
from pathlib import Path
import streamlit as st
from google import genai
from dotenv import load_dotenv

load_dotenv()

def obter_chave_api():
    """Recupera a chave da API respeitando o ambiente, com proteção contra falhas locais."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
        
    return os.getenv("GEMINI_API_KEY")

@st.cache_resource(ttl="47h", show_spinner=False)

def carregar_base_conhecimento():
    """
    Lê a pasta base_conhecimento/, faz upload dos PDFs para a API do Gemini
    e retorna um dicionário com os objetos de arquivo prontos para uso.
    """
    diretorio_base = Path("base_conhecimento")
    arquivos_prontos = []
    
    if not diretorio_base.exists():
        st.warning("⚠️ Pasta 'base_conhecimento' não encontrada. A IA responderá sem contexto jurídico.")
        return arquivos_prontos

    pdfs = list(diretorio_base.glob("*.pdf"))
    
    if not pdfs:
        return arquivos_prontos

    chave = obter_chave_api()
    if not chave:
        st.error("Erro: Chave da API do Gemini não encontrada.")
        return arquivos_prontos
        
    client = genai.Client(api_key=chave)

    with st.spinner("📚 Sincronizando Normas Regulamentadoras com o Motor de IA..."):
        for pdf_path in pdfs:
            try:
                arquivo_gemini = client.files.upload(
                    file=str(pdf_path),
                    config={"display_name": pdf_path.name}
                )
                arquivos_prontos.append(arquivo_gemini)
            except Exception as e:
                st.error(f"Erro ao fazer upload do arquivo {pdf_path.name}: {e}")
                
    return arquivos_prontos

def listar_nomes_documentos(arquivos_gemini):
    """Função auxiliar para a Dashboard exibir quais NRs estão ativas."""
    return [arquivo.display_name for arquivo in arquivos_gemini]