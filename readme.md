# AI-Driven Support Triage: Analisador Inteligente de Chamados 🤖🚀

Este projeto demonstra a aplicação prática de **Inteligência Artificial (NLP)** e **Engenharia de Dados** para otimizar fluxos de atendimento técnico e suporte, alinhando-se aos requisitos de análise de sistemas e suprimento de IA.

## 🎯 Objetivo
Automatizar a triagem e classificação de chamados técnicos utilizando Processamento de Linguagem Natural (NLP). O sistema analisa o tom emocional do relato do usuário para definir prioridades críticas instantaneamente e preparar os dados para modelos de linguagem (LLMs).

## 🛠️ Funcionalidades
- **Data Cleaning & Quality:** Tratamento de dados brutos, remoção de ruídos e padronização de textos utilizando a biblioteca **Pandas**.
- **Sentiment Analysis (IA):** Implementação de inteligência artificial para detectar urgência e termos críticos nos relatos, elevando a prioridade de chamados automaticamente através de análise de sentimento.
- **AI Supply (Suprimento de IA):** Estruturação de dados em formatos otimizados para Engenharia de Prompt, prontos para integração com APIs de IA de larga escala.
- **Automação de Relatórios:** Geração de arquivos CSV inteligentes que permitem aos gestores focar nos problemas de maior impacto.

## 💻 Tecnologias
- **Linguagem:** Python 3.x
- **Bibliotecas:** Pandas (Dados) e TextBlob (IA/NLP)
- **Controle de Versão:** Git

## 🔄 Personalização e Escalabilidade

O projeto foi estruturado de forma modular para que os dados de teste possam ser facilmente substituídos por fontes reais de produção:

- **Arquivos Externos:** Para analisar seus próprios chamados, basta substituir a estrutura de dicionário inicial por uma leitura de arquivo CSV ou Excel:
  ```python
  df = pd.read_csv('seus_chamados.csv')
  
## 🚀 Como executar
1. Instale as dependências: 
   ```bash
   pip install pandas textblob

2. Execute o script principal
    ```bash
    python main.py