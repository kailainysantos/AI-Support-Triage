# AI-Driven Support Triage: Analisador Inteligente de Chamados 🤖🚀

Este projeto utiliza **Processamento de Linguagem Natural (NLP)** e **Engenharia de Dados** para automatizar a triagem de chamados técnicos, classificando-os por prioridade crítica instantaneamente.

## 🎯 Objetivo
Reduzir o tempo de resposta do suporte técnico, identificando urgências através de análise de tom emocional e termos técnicos críticos em relatos de usuários.

## 🛠️ Funcionalidades e Melhorias
- **CLI Dinâmica:** Agora o script aceita arquivos CSV externos via linha de comando (`--input` e `--output`).
- **Lógica de Sentimento Refinada:** Combinação de análise de polaridade (`TextBlob`) com detecção de gatilhos críticos específicos para o cenário de TI.
- **Integração com Gemini API:** Geração automática de sugestões de solução técnica utilizando IA Generativa (opcional).
- **Tratamento de Erros:** Validação de colunas e suporte a codificação UTF-8 para garantir que acentos e caracteres especiais não quebrem o processamento.

## 💻 Tecnologias
- **Linguagem:** Python 3.x
- **Bibliotecas:** Pandas, TextBlob, Google Generative AI
- **Controle de Versão:** Git

## 🚀 Como executar

1. **Instale as dependências:** 
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute com os dados de exemplo:**
    ```bash
    python main.py
    ```

3. **Execute com seus próprios dados (CSV):**
    ```bash
    python main.py --input seus_chamados.csv --output relatorio_final.csv
    ```

4. **[AVANÇADO] Gerar sugestões com IA (Gemini):**
    Primeiro, defina sua chave de API como uma variável de ambiente:
    - **Windows:** `set GEMINI_API_KEY=sua_chave_aqui`
    - **Linux/Mac:** `export GEMINI_API_KEY=sua_chave_aqui`
    
    Depois execute com a flag `--ai`:
    ```bash
    python main.py --ai
    ```

## 📈 Próximos Passos (Roadmap)
- [ ] **Dashboard Streamlit:** Visualização gráfica da volumetria de chamados por prioridade.
- [ ] **Modelos Específicos para PT-BR:** Implementação do SpaCy ou Transformers para análise semântica mais profunda em português.
- [ ] **Interface Web:** Uma página simples para colar relatos e receber a triagem na hora.