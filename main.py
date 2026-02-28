import argparse
import sys
import os
import asyncio
import pandas as pd
from core.engine import processar_chamados_lote
from utils.logger import get_logger

logger = get_logger("main")

async def async_main():
    parser = argparse.ArgumentParser(description="AI-Driven Support Triage - Analisador de Chamados")
    parser.add_argument("--input", help="Caminho para o arquivo CSV de entrada", default=None)
    parser.add_argument("--output", help="Caminho para salvar o CSV de saída", default="relatorio_prioridade.csv")
    parser.add_argument("--ai", action="store_true", help="Ativar geração de solução e classificação avançada via Gemini API")
    
    args = parser.parse_args()

    # 1. CARREGAMENTO DE DADOS
    if args.input and os.path.exists(args.input):
        logger.info(f"📂 Carregando dados de: {args.input}")
        try:
            df = pd.read_csv(args.input)
            if 'relato' not in df.columns:
                logger.error("❌ Erro: O CSV deve conter uma coluna chamada 'relato'.")
                sys.exit(1)
        except Exception as e:
            logger.error(f"❌ Erro ao ler o arquivo: {e}")
            sys.exit(1)
    else:
        logger.info("💡 Usando dados de exemplo...")
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

    # 2. PROCESSAMENTO
    df = await processar_chamados_lote(df, usar_ai=args.ai)

    # 3. EXIBIÇÃO E EXPORTAÇÃO
    print("\n" + "="*80)
    print("                      RESULTADO DA TRIAGEM INTELIGENTE")
    print("="*80)
    pd.set_option('display.max_colwidth', 50)
    colunas_exibir = ['cliente', 'prioridade_automatica', 'categoria_ia', 'relato']
    print(df[colunas_exibir])
    print("="*80)

    try:
        df.to_csv(args.output, index=False, encoding='utf-8-sig')
        logger.info(f"✅ Relatório gerado com sucesso: {args.output}")
    except Exception as e:
        logger.error(f"❌ Erro ao salvar o arquivo: {e}")

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
