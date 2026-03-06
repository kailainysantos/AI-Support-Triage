import pandas as pd
import asyncio
from textblob import TextBlob
from config.settings import GATILHOS_CRITICOS
from services.gemini_service import analisar_chamado_llm
from utils.logger import get_logger

logger = get_logger(__name__)

def analisar_prioridade_basica(texto: str) -> str:
    """
    Analisa a prioridade com base no sentimento (TextBlob) 
    e palavras-chave críticas. Método fallback/rápido.
    """
    if not isinstance(texto, str):
        return "Indefinida"
    
    analise = TextBlob(texto)
    texto_lower = texto.lower()
    
    if analise.sentiment.polarity < -0.3 or any(g in texto_lower for g in GATILHOS_CRITICOS):
        return "🔴 IMEDIATA (Crítico)"
    elif analise.sentiment.polarity < 0 or "lento" in texto_lower or "ajuda" in texto_lower:
        return "🟡 MÉDIA"
    else:
        return "🟢 BAIXA"

async def processar_chamados_lote(df: pd.DataFrame, usar_ai: bool) -> pd.DataFrame:
    """
    Processa um DataFrame de chamados.
    Se usar_ai for True, faz consultas assíncronas ao Gemini para obter
    prioridade unificada, categoria e solução.
    Caso contrário, usa o método básico via TextBlob.
    """
    if usar_ai:
        logger.info("🤖 Iniciando processamento avançado via LLM (Gemini)...")
        tasks = [analisar_chamado_llm(relato) for relato in df['relato']]
        resultados = await asyncio.gather(*tasks)
        
        prioridades = []
        categorias = []
        solucoes = []
        
        for res in resultados:
            prioridades.append(res['prioridade'])
            categorias.append(res['categoria'])
            solucoes.append(res['solucao'])
            
        df['prioridade_automatica'] = prioridades
        df['categoria_ia'] = categorias
        df['solucao_sugerida'] = solucoes
    else:
        logger.info("🤖 Iniciando processamento básico via TextBlob/Keywords...")
        df['prioridade_automatica'] = df['relato'].apply(analisar_prioridade_basica)
        df['categoria_ia'] = "N/A (AI desativada)"
        df['solucao_sugerida'] = "Rode com --ai para gerar soluções e categorias."

    return df
