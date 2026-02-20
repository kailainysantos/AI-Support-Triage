import pandas as pd
from textblob import TextBlob
import argparse
import sys
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

def analisar_prioridade_ia(texto):
    """
    Analisa a prioridade com base no sentimento (TextBlob) 
    e palavras-chave críticas.
    """
    if not isinstance(texto, str):
        return "Indefinida"
    
    analise = TextBlob(texto)
    texto_lower = texto.lower()
    gatilhos_criticos = ["crítico", "parou", "urgente", "emergência", "erro grave", "não funciona", "desesperado"]
    
    if analise.sentiment.polarity < -0.3 or any(g in texto_lower for g in gatilhos_criticos):
        return "🔴 IMEDIATA (Crítico)"
    elif analise.sentiment.polarity < 0 or "lento" in texto_lower or "ajuda" in texto_lower:
        return "🟡 MÉDIA"
    else:
        return "🟢 BAIXA"

def gerar_solucao_ia(relato):
    """
    Gera uma sugestão de solução usando a API do Gemini.
    """
    if not model:
        return "⚠️ (Gemini não configurado)"
    
    prompt = f"Você é um especialista em suporte técnico de TI. Sugira uma solução curta e profissional para o seguinte chamado: '{relato}'"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Erro na IA: {str(e)[:50]}..."

def main():
    parser = argparse.ArgumentParser(description="AI-Driven Support Triage - Analisador de Chamados")
    parser.add_argument("--input", help="Caminho para o arquivo CSV de entrada", default=None)
    parser.add_argument("--output", help="Caminho para salvar o CSV de saída", default="relatorio_prioridade.csv")
    parser.add_argument("--ai", action="store_true", help="Ativar geração de solução via Gemini API")
    
    args = parser.parse_args()

    # 1. CARREGAMENTO DE DADOS
    if args.input and os.path.exists(args.input):
        print(f"📂 Carregando dados de: {args.input}")
        try:
            df = pd.read_csv(args.input)
            if 'relato' not in df.columns:
                print("❌ Erro: O CSV deve conter uma coluna chamada 'relato'.")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Erro ao ler o arquivo: {e}")
            sys.exit(1)
    else:
        print("💡 Usando dados de exemplo...")
        dados_suporte = {
            'cliente': ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena'],
            'relato': [
                'O sistema está um pouco lento hoje.',
                'ESTOU DESESPERADO! O servidor caiu e parou a fábrica toda!!',
                'Gostaria de saber como mudo minha foto de perfil.',
                'Erro crítico no banco de dados, não consigo salvar nada.',
                'Preciso de ajuda com a redefinição de senha.'
            ]
        }
        df = pd.DataFrame(dados_suporte)

    # 2. PROCESSAMENTO (Motor de IA)
    print("🤖 IA processando os relatos e calculando prioridades...")
    df['prioridade_automatica'] = df['relato'].apply(analisar_prioridade_ia)

    # 3. GERAÇÃO DE SOLUÇÃO (Gemini)
    if args.ai:
        if model:
            print("🧠 Consultando Gemini para sugestões de solução...")
            df['solucao_sugerida'] = df['relato'].apply(gerar_solucao_ia)
        else:
            print("⚠️ Aviso: GEMINI_API_KEY não encontrada no arquivo .env.")
            df['solucao_sugerida'] = "Chave não configurada."
    else:
        df['solucao_sugerida'] = "Rode com --ai para gerar soluções."

    # 4. EXIBIÇÃO E EXPORTAÇÃO
    print("\n" + "="*50)
    print("      RESULTADO DA TRIAGEM INTELIGENTE")
    print("="*50)
    pd.set_option('display.max_colwidth', 50)
    print(df[['cliente', 'prioridade_automatica', 'relato']])
    print("="*50)

    try:
        df.to_csv(args.output, index=False, encoding='utf-8-sig')
        print(f"\n✅ Relatório gerado com sucesso: {args.output}")
    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo: {e}")

if __name__ == "__main__":
    main()
