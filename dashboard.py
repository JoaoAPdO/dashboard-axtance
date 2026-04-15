import streamlit as st
import pandas as pd
from dados import obter_dados_planilha
from ia_engine import preparar_contexto_ia, gerar_diagnostico_ia 

# --- CONSTANTES ---
COLUNAS_LIXO = [
    'Timestamp', 
    'Pouso Alegre/MG', 
    'Concordo com os termos e normas presentes acima'
]

PERGUNTAS_ABERTAS = [
    'Nome completo',
    'Cargo a ser ocupado',
    'Ao todo quantas pessoas moram com você?',
    'Quanto tempo reside no último endereço?',
    'Sua pressão é',
    'Quando foi sua ultima consulta médica',
    'Qual era a especialidade do médico',
    'Quais motivos te levaram ao médico?',
    'Com que frequência vai ao médico',
    'Qual comida você mais gosta?',
    'Qual é o alimento que você mais consome no dia a dia?',    
    'Qual sua bebida favorita?',
    'Com que frequência você a toma?',
    'O que você gosta de fazer quando está de folga do trabalho?',
    'Descreva a rotina de seu trabalho em um dia',
    'Como você lida com situações de pressão ou conflito?',
    'Como lidou?',
    'Como você reage diante de situações inesperadas ou emergenciais?',
]

def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Remove as colunas indesejadas listadas nas constantes."""
    colunas_remover = [c for c in COLUNAS_LIXO if c in df.columns]
    return df.drop(columns=colunas_remover)

def renderizar_cabecalho():
    """Mostra o título principal e o botão de atualização de cache."""
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("📊 Dashboard - Inventário de Risco Ocupacional")
    with col2:
        st.write("") 
        if st.button("🔄 Atualizar Dados"):
            st.cache_data.clear() 
            st.rerun()
    st.markdown("---")

def renderizar_aba_visao_geral(df: pd.DataFrame):
    """Renderiza a aba 1 com indicadores chave e perfil."""
    st.subheader("Perfil dos Respondentes")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'Sexo' in df.columns:
            st.write("**Distribuição por Sexo**")
            dados_sexo = df['Sexo'].value_counts().reset_index()
            dados_sexo.columns = ['Sexo', 'Quantidade']
            st.bar_chart(dados_sexo, x='Sexo', y='Quantidade')
            
    with col2:
        if 'Estado Civil' in df.columns:
            st.write("**Estado Civil**")
            dados_civil = df['Estado Civil'].value_counts().reset_index()
            dados_civil.columns = ['Estado Civil', 'Quantidade']
            st.bar_chart(dados_civil, x='Estado Civil', y='Quantidade')
            
    with col3:
        if 'Cargo a ser ocupado' in df.columns:
            st.write("**Cargos**")
            dados_cargo = df['Cargo a ser ocupado'].value_counts().reset_index()
            dados_cargo.columns = ['Cargo', 'Quantidade']
            st.bar_chart(dados_cargo, x='Cargo', y='Quantidade')
            
    st.markdown("---")
    st.info("💡 Utilize a aba 'Análise Detalhada' para cruzar e explorar todas as outras perguntas.")

def renderizar_aba_analise_detalhada(df: pd.DataFrame):
    """Renderiza a aba 2 com o filtro de gráficos dinâmicos."""
    st.subheader("📈 Análise Interativa")
    
    opcoes_multipla_escolha = [col for col in df.columns if col not in PERGUNTAS_ABERTAS]

    perguntas_selecionadas = st.multiselect(
        "Selecione as perguntas que deseja comparar:", 
        opcoes_multipla_escolha,
        default=opcoes_multipla_escolha[0] if opcoes_multipla_escolha else None
    )

    if perguntas_selecionadas:
        cols = st.columns(2)
        for i, pergunta in enumerate(perguntas_selecionadas):
            with cols[i % 2]:
                st.write(f"**{pergunta}**")
                contagem = df[pergunta].value_counts().reset_index()
                contagem.columns = ['Resposta', 'Quantidade']
                st.bar_chart(contagem, x='Resposta', y='Quantidade')
                st.markdown("---")
    else:
        st.info("Selecione pelo menos uma pergunta no menu acima.")

def renderizar_aba_dados_crus(df: pd.DataFrame):
    """Renderiza a aba 3 com a tabela do Pandas crua."""
    st.subheader("Visualização dos Dados Crus")
    st.dataframe(df, use_container_width=True)

def renderizar_aba_diagnostico_ia(df: pd.DataFrame):
    """Renderiza a aba 4 com a integração do Gemini para diagnóstico estratégico."""
    st.subheader("🤖 Diagnóstico Estratégico com IA")
    st.write("""
        Esta aba utiliza Inteligência Artificial para analisar as tendências estatísticas 
        e os comentários qualitativos da pesquisa, gerando recomendações consultivas.
    """)
    
    if st.button("🚀 Gerar Diagnóstico com Gemini", type="primary"):
        with st.spinner("O motor de IA está processando os dados e elaborando o plano de ação..."):
            contexto = preparar_contexto_ia(df, PERGUNTAS_ABERTAS)
            
            if "Erro" in contexto or "Aviso:" in contexto:
                st.warning(contexto)
            else:
                diagnostico = gerar_diagnostico_ia(contexto)
                
                if "Erro" in diagnostico:
                    st.error(diagnostico)
                else:
                    st.success("Diagnóstico gerado com sucesso!")
                    with st.container(border=True):
                        st.markdown(diagnostico)

def main():
    st.set_page_config(page_title="Dashboard Axtance", layout="wide", page_icon="📊")
    
    renderizar_cabecalho()

    with st.spinner("A carregar base de dados..."):
        df = obter_dados_planilha()

    if not df.empty:
        df = limpar_dados(df)
        st.metric(label="Total de Respostas Coletadas", value=len(df))
        
        aba1, aba2, aba3, aba4 = st.tabs([
            "📊 Visão Geral", 
            "📈 Análise Detalhada", 
            "📄 Dados Crus", 
            "🤖 Diagnóstico IA"
        ])
        
        with aba1:
            renderizar_aba_visao_geral(df)
        with aba2:
            renderizar_aba_analise_detalhada(df)
        with aba3:
            renderizar_aba_dados_crus(df)
        with aba4:
            renderizar_aba_diagnostico_ia(df)
    else:
        st.error("❌ Ocorreu um erro ao carregar os dados ou a planilha está vazia. Verifique a conexão.")

if __name__ == "__main__":
    main()