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

def gerar_diagnostico_ia(contexto_dados, arquivos_conhecimento=None):
    """
    Conecta ao Gemini-2.5-Flash via STREAMING.
    Transformada em um gerador nativo para manter a conexão HTTP ativa
    até que o Streamlit termine de desenhar o texto na tela.
    """
    if arquivos_conhecimento is None:
        arquivos_conhecimento = []

    api_key = obter_chave_gemini()
    if not api_key:
        yield "❌ Erro: Chave de API não configurada corretamente."
        return

    try:
        client = genai.Client(api_key=api_key)
        
        prompt_sistema = """Você é um Consultor Sênior em RH, Saúde Ocupacional e Compliance Trabalhista no Brasil.
Analise os dados fornecidos e gere um diagnóstico estratégico em Markdown contendo:
1. **Visão Geral:** Resumo do cenário atual.
2. **Fortalezas:** O que está funcionando bem e deve ser mantido.
3. **Riscos e Alertas (Jurídicos/Ocupacionais):** Pontos críticos de atenção.
4. **Plano de Ação:** 3 passos práticos para melhoria.

⚠️ REGRA CRUCIAL 1 (INTERPRETAÇÃO):
A pesquisa usa uma escala onde o valor MÍNIMO (ex: 1) = "Nunca" e MAIORES (ex: 5) = "Sempre".
- Média BAIXA em perguntas negativas (dores, acidentes) é EXCELENTE (não ocorre).
- Média ALTA em perguntas negativas é RISCO CRÍTICO.

📚 REGRA CRUCIAL 2 (EMBASAMENTO LEGAL - NRs):
Você receberá arquivos contendo a Legislação Trabalhista (Normas Regulamentadoras - NRs). 
Baseie seu diagnóstico e plano de ação ESTRITAMENTE nestes documentos e nos dados da pesquisa. 
Sempre que recomendar uma ação ou identificar um risco grave, CITE OBRIGATORIAMENTE a norma e o item correspondente (Ex: "Segundo a NR-17, item X...", "De acordo com o PCMSO da NR-07..."). Não invente normas ou leis que não estejam nos documentos anexados.

Seja direto, técnico e profissional."""
        
        configuracao = types.GenerateContentConfig(
            system_instruction=prompt_sistema,
            temperature=0.3, 
        )

        conteudo_chamada = arquivos_conhecimento + [contexto_dados]

        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=conteudo_chamada, 
            config=configuracao      
        )
        
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"❌ Erro na comunicação com a IA: {str(e)}"