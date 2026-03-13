import pytest
import pandas as pd
from core.engine import analisar_prioridade_basica

def test_prioridade_basica_critica():
    texto = "O servidor parou e estamos em emergência total!"
    prioridade = analisar_prioridade_basica(texto)
    assert "🔴 IMEDIATA" in prioridade

def test_prioridade_basica_media():
    texto = "O sistema está um pouco lento hoje e preciso de ajuda."
    prioridade = analisar_prioridade_basica(texto)
    assert "🟡 MÉDIA" in prioridade

def test_prioridade_basica_baixa():
    texto = "Como faço para alterar a fonte do relatório?"
    prioridade = analisar_prioridade_basica(texto)
    assert "🟢 BAIXA" in prioridade

def test_prioridade_basica_texto_invalido():
    prioridade = analisar_prioridade_basica(None)
    assert prioridade == "Indefinida"
