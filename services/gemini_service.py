import json
import google.generativeai as genai
from config.settings import GEMINI_API_KEY, MODEL_NAME, LLM_SYSTEM_PROMPT
from utils.logger import get_logger

logger = get_logger(__name__)

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
else:
    model = None

async def analisar_chamado_llm(relato: str) -> dict:
    """
    Usa o Gemini de forma assíncrona para extrair prioridade, categoria e solução.
    """
    if not model:
        return {
            "prioridade": "⚠️ (Gemini não config)",
            "categoria": "Desconhecida",
            "solucao": "Chave GEMINI_API_KEY não configurada."
        }

    prompt = LLM_SYSTEM_PROMPT.format(relato=relato)
    
    try:
        response = await model.generate_content_async(prompt)
        text = response.text.strip()
        
        # Remove eventuais marcações de markdown de código
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        data = json.loads(text.strip())
        return {
            "prioridade": data.get("prioridade", "Indefinida"),
            "categoria": data.get("categoria", "Indefinida"),
            "solucao": data.get("solucao", "")
        }
    except Exception as e:
        logger.error(f"Erro ao consultar Gemini para o relato '{relato[:20]}...': {e}")
        return {
            "prioridade": "❌ Erro IA",
            "categoria": "Erro",
            "solucao": f"Falha na análise: {str(e)[:50]}..."
        }
