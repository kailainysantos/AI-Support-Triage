import streamlit as st
import pandas as pd
import asyncio
import os
from dotenv import load_dotenv

# Carrega ambiente antes de importar módulos que dependem dele
load_dotenv()

from core.engine import processar_chamados_lote, analisar_prioridade_basica
from services.gemini_service import analisar_chamado_llm

st.set_page_config(
    page_title="AI Support Triage",
    page_icon="🤖",
    layout="wide"
)

# --- Funções Assíncronas ---
async def processar_csv(df, usar_ai):
    return await processar_chamados_lote(df, usar_ai=usar_ai)

async def processar_texto(texto, usar_ai):
    if usar_ai:
        resultado = await analisar_chamado_llm(texto)
        return resultado['prioridade'], resultado['categoria'], resultado['solucao']
    else:
        prioridade = analisar_prioridade_basica(texto)
        return prioridade, "N/A (AI desativada)", "Ative a IA para gerar soluções."

# --- Interface Principal ---
st.title("🤖 AI-Driven Support Triage Dashboard")
st.markdown("Analise e classifique chamados técnicos instantaneamente usando regras de NLP e **Google Gemini**.")

st.sidebar.header("⚙️ Configurações")
usar_ai = st.sidebar.checkbox("Ativar IA (Gemini)", value=True, help="Usa a IA para classificar prioridade, categoria e sugerir soluções.")

if usar_ai and not os.getenv("GEMINI_API_KEY"):
    st.sidebar.error("⚠️ Chave da API do Gemini não encontrada no arquivo .env!")

tab_lote, tab_individual = st.tabs(["📂 Processamento em Lote (CSV)", "💬 Análise Individual"])

# --- TAB 1: Processamento em Lote ---
with tab_lote:
    st.markdown("### Faça upload de um arquivo CSV contendo os chamados")
    st.markdown("O arquivo deve conter uma coluna chamada **`relato`**.")
    
    arquivo_csv = st.file_uploader("Upload CSV", type=["csv"])
    
    if arquivo_csv is not None:
        try:
            df_entrada = pd.read_csv(arquivo_csv)
            
            if 'relato' not in df_entrada.columns:
                st.error("❌ O arquivo CSV deve conter uma coluna chamada 'relato'.")
            else:
                st.info(f"Arquivo carregado com sucesso. {len(df_entrada)} registros encontrados.")
                
                if st.button("🚀 Processar Chamados", type="primary"):
                    with st.spinner("Analisando chamados... isso pode levar alguns segundos."):
                        df_resultado = asyncio.run(processar_csv(df_entrada, usar_ai))
                    
                    st.success("✅ Processamento concluído!")
                    
                    # Exibir tabela de resultados
                    st.dataframe(df_resultado, use_container_width=True)
                    
                    # Converter para CSV para download
                    csv_export = df_resultado.to_csv(index=False, encoding='utf-8-sig').encode('utf-8')
                    st.download_button(
                        label="📥 Baixar Relatório Completo",
                        data=csv_export,
                        file_name="relatorio_prioridade.csv",
                        mime="text/csv",
                    )
                    
                    # Dashboard Visual
                    st.markdown("---")
                    st.subheader("📊 Visualização de Dados")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Distribuição por Prioridade**")
                        # Usando Streamlit nativo (bar chart) ou metrics
                        p_counts = df_resultado['prioridade_automatica'].value_counts()
                        st.bar_chart(p_counts)
                    
                    with col2:
                        if 'categoria_ia' in df_resultado.columns and usar_ai:
                            st.markdown("**Distribuição por Categoria**")
                            c_counts = df_resultado['categoria_ia'].value_counts()
                            st.bar_chart(c_counts)

        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

# --- TAB 2: Análise Individual ---
with tab_individual:
    st.markdown("### Teste rápido: Cole um relato de chamado")
    
    texto_relato = st.text_area("Descreva o problema:", height=150, placeholder="Ex: O servidor do banco de dados caiu e a fábrica inteira está parada. Socorro!")
    
    if st.button("🔍 Analisar", type="primary"):
        if not texto_relato.strip():
            st.warning("Por favor, digite um relato para analisar.")
        else:
            with st.spinner("Analisando relato..."):
                prioridade, categoria, solucao = asyncio.run(processar_texto(texto_relato, usar_ai))
            
            # Estilização baseada na prioridade
            cor = "green"
            if "IMEDIATA" in prioridade:
                cor = "red"
            elif "MÉDIA" in prioridade:
                cor = "orange"
                
            st.markdown(f"### Prioridade: <span style='color:{cor}'>{prioridade}</span>", unsafe_allow_html=True)
            if usar_ai:
                st.markdown(f"**Categoria Detectada:** `{categoria}`")
            
            st.info(f"**💡 Solução Sugerida:**\\n{solucao}")
