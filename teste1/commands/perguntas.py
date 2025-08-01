import json
import os

def carregar_perguntas():
    arquivo_perguntas = os.path.join(os.path.dirname(__file__), "perguntas1.json")
    with open(arquivo_perguntas, "r", encoding="utf-8") as f:
        data = json.load(f)
        perguntas_formatadas = []

        for item in data["perguntas_respostas"]:
            pergunta = item["pergunta"]
            resposta = item["resposta"].strip().lower()
            perguntas_formatadas.append((pergunta, resposta))

        return perguntas_formatadas

def salvar_perguntas(perguntas_respostas):
    with open("commands/perguntas1.json", "w", encoding="utf-8") as f:
        json.dump({"perguntas_respostas": perguntas_respostas}, f, indent=4, ensure_ascii=False)

perguntas_respostas = carregar_perguntas()
