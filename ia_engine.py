import os
import pandas as pd
import streamlit as st
from google import genai
from google.genai import types 
from dotenv import load_dotenv

load_dotenv()

def obter_chave_gemini():
    """
    Implementa a Segurança Híbrida:
    1º Tenta buscar do .env (Local)
    2º Se falhar, busca do st.secrets (Nuvem/Streamlit Cloud)
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except (KeyError, AttributeError):
            return None
            
    return api_key

def preparar_contexto_ia(df, perguntas_abertas):
    """
    Resume o DataFrame em um texto estruturado para a API.
    Apresenta os dados numéricos de forma neutra para a IA interpretar o contexto.
    """
    try:
        df_processado = df.copy()
        
        for col in df_processado.columns:
            if col not in perguntas_abertas:
                try:
                    df_processado[col] = pd.to_numeric(df_processado[col])
                except (ValueError, TypeError):
                    pass 

        colunas_numericas = df_processado.select_dtypes(include=['number', 'float', 'int']).columns.tolist()
        colunas_categoricas = [c for c in df_processado.columns if c not in perguntas_abertas and c not in colunas_numericas]
        
        if not colunas_numericas and not colunas_categoricas:
            return "Aviso: Não foram encontradas perguntas de múltipla escolha ou notas para analisar."

        contexto = "📋 RESUMO ESTATÍSTICO DA PESQUISA:\n\n"

        if colunas_numericas:
            medias = df_processado[colunas_numericas].mean().sort_values(ascending=False)
            contexto += "📊 TENDÊNCIA DE FREQUÊNCIA (Médias das respostas numéricas):\n"
            contexto += "Maiores Médias (Itens que ocorrem com mais frequência / Concordância alta):\n"
            contexto += f"{medias.head(5).to_string()}\n\n"
            contexto += "Menores Médias (Itens que ocorrem com menos frequência / Concordância baixa):\n"
            contexto += f"{medias.tail(5).to_string()}\n\n"

        if colunas_categoricas:
            contexto += "📈 TENDÊNCIAS CATEGÓRICAS (Respostas mais frequentes):\n"
            for col in colunas_categoricas:
                top_resposta = df_processado[col].value_counts().head(1)
                if not top_resposta.empty:
                    contexto += f"  * {col}: Maioria respondeu '{top_resposta.index[0]}' ({top_resposta.values[0]} votos)\n"
            contexto += "\n"

        resumo_abertas = ""
        for pergunta in perguntas_abertas:
            if pergunta in df.columns:
                respostas_validas = df[pergunta].dropna()
                respostas_validas = respostas_validas[respostas_validas.astype(str).str.strip() != ""]
                if not respostas_validas.empty:
                    amostra = respostas_validas.sample(n=min(3, len(respostas_validas))).tolist()
                    resumo_abertas += f"Tema - {pergunta}:\n"
                    for resp in amostra:
                        resumo_abertas += f'  - "{resp}"\n'

        contexto += "🗣️ VOZ DOS COLABORADORES (Amostras qualitativas):\n"
        contexto += resumo_abertas if resumo_abertas else "Nenhum comentário registrado."

        return contexto.strip()

    except Exception as e:
        return f"Erro ao processar dados: {str(e)}"

def gerar_diagnostico_ia(contexto_dados):
    """
    Conecta ao Gemini-3-Flash-Preview e gera o diagnóstico estratégico estruturado.
    Contém regras rígidas de interpretação de escala.
    """
    api_key = obter_chave_gemini()
    if not api_key:
        return "Erro: Chave de API não configurada corretamente."

    try:
        client = genai.Client(api_key=api_key)
        
        prompt_sistema = """Você é um Consultor Sênior em RH e Segurança do Trabalho.
Analise os dados fornecidos e gere um diagnóstico estratégico em Markdown contendo:
1. **Visão Geral:** Resumo do cenário atual.
2. **Fortalezas:** O que está funcionando bem e deve ser mantido.
3. **Riscos e Alertas:** Pontos críticos de atenção imediata.
4. **Plano de Ação:** 3 passos práticos para melhoria.

⚠️ REGRA CRUCIAL DE INTERPRETAÇÃO DOS DADOS:
As perguntas da pesquisa utilizam uma escala onde o valor MÍNIMO (ex: 1) significa "Nunca" e valores MAIORES (ex: 4 ou 5) significam "Com muita frequência".
- Uma média BAIXA (ex: 1.0) em perguntas negativas (como dores, desmaios, estresse) é um PONTO FORTE (excelente, pois não ocorre).
- Uma média ALTA em perguntas negativas é um RISCO CRÍTICO.
Use seu raciocínio lógico para interpretar se a média de cada item é positiva ou negativa com base no contexto da pergunta.

Seja direto, profissional e baseie-se estritamente nos dados fornecidos."""
        
        configuracao = types.GenerateContentConfig(
            system_instruction=prompt_sistema,
            temperature=0.3, 
        )

        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=contexto_dados, 
            config=configuracao      
        )
        
        return response.text

    except Exception as e:
        return f"Erro na comunicação com a IA: {str(e)}"