import pandas as pd
import streamlit as st
from conexao import inicializar_conexao

@st.cache_data(ttl=600, show_spinner=False)
def obter_dados_planilha():
    """
    Solicita a aba conectada, extrai todos os valores e retorna um DataFrame do Pandas.
    Trata automaticamente colunas com nomes duplicados.
    """
    aba = inicializar_conexao()
    
    if aba is None:
        return pd.DataFrame() 
        
    try:
        dados_brutos = aba.get_all_values()
        
        if not dados_brutos:
            st.warning("⚠️ A planilha está vazia.")
            return pd.DataFrame()

        cabecalhos_originais = dados_brutos[0]
        linhas = dados_brutos[1:]
        
        cabecalhos_unicos = []
        contagem = {}
        
        for coluna in cabecalhos_originais:
            if coluna in contagem:
                contagem[coluna] += 1
                cabecalhos_unicos.append(f"{coluna} ({contagem[coluna]})")
            else:
                contagem[coluna] = 0
                cabecalhos_unicos.append(coluna)
        
        df = pd.DataFrame(linhas, columns=cabecalhos_unicos)
        return df
        
    except Exception as e:
        st.error(f"❌ Erro ao extrair dados da planilha: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    print("📥 Iniciando extração de dados...")
    meu_dataframe = obter_dados_planilha()
    
    if not meu_dataframe.empty:
        print(f"✅ Sucesso! Total de respostas carregadas: {len(meu_dataframe)}")
        print("\n--- Primeiras linhas ---")
        print(meu_dataframe.head(3))
    else:
        print("❌ Falha: O DataFrame retornou vazio.")