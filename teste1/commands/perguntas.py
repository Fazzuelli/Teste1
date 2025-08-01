import json
import os

def carregar_perguntas():
    caminho = os.path.join(os.path.dirname(__file__), "perguntas1.json")
    with open(caminho, "r", encoding="utf-8") as f:
        data = json.load(f)
        perguntas_formatadas = []

        for item in data["perguntas_respostas"]:
            pergunta = item["pergunta"]
            resposta = item["resposta"].strip().lower()
            perguntas_formatadas.append((pergunta, resposta))

        return perguntas_formatadas

perguntas_respostas = carregar_perguntas()
