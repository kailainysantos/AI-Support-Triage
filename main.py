import pandas as pd
from textblob import TextBlob

# 1. DADOS BRUTOS
dados_suporte = {
    'cliente': ['Ana', 'Bruno', 'Carla', 'Diego'],
    'relato': [
        'O sistema está um pouco lento hoje.',
        'ESTOU DESESPERADO! O servidor caiu e parou a fábrica toda!!',
        'Gostaria de saber como mudo minha foto de perfil.',
        'Erro crítico no banco de dados, não consigo salvar nada.'
    ]
}

df = pd.DataFrame(dados_suporte)

# 2. O MOTOR DE IA (Suprimento e Inteligência)
def analisar_prioridade_ia(texto):
    # A IA analisa o sentimento: quanto mais negativo/urgente o tom, menor a polaridade
    analise = TextBlob(texto)
    # Traduzimos o sentimento em prioridade real
    if analise.sentiment.polarity < -0.1 or "crítico" in texto.lower() or "parou" in texto.lower():
        return "IMEDIATA (IA detectou Urgência)"
    elif analise.sentiment.polarity < 0:
        return "Média"
    else:
        return "Baixa"

print("🤖 IA processando os relatos...")
df['prioridade_automatica'] = df['relato'].apply(analisar_prioridade_ia)

# 3. SUPRIMENTO PARA MODELOS MAIORES
df['prompt_final'] = df.apply(lambda x: f"Sugira uma solução técnica para: {x['relato']}", axis=1)

# EXIBIÇÃO
print("\n--- Resultado da Triagem Inteligente ---")
print(df[['relato', 'prioridade_automatica']])

# Exportando para mostrar ao gestor
df.to_csv('suporte_ia_avancado.csv', index=False)