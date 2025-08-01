import discord
from discord import app_commands
import random
import os
import json
import openai
from keys import keys
from openai import OpenAI
from commands.perguntas import perguntas_respostas
import commands.perguntas as perguntas
from commands.ranking import registrar_comandos_ranking
from commands.dado import registrar_comando_dado
from commands.soma import registrar_comando_soma
from commands.jogo import registrar_comando_jogo
from commands.comandos_adicionar import registrar_comando_adicionar_pergunta

TOKEN_DISCORD = keys.get("token")

# Arquivo de ranking
ranking_file = "commands/ranking.json"
 # Arquivo de dados do dado
dados_dado_file = "commands/dados_maximos.json"

def carregar_ranking():
    if os.path.exists(ranking_file):
        with open(ranking_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_ranking(ranking):
    with open(ranking_file, "w", encoding="utf-8") as f:
        json.dump(ranking, f, indent=4)

def carregar_dados_dado():
    if os.path.exists(dados_dado_file):
        with open(dados_dado_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_dados_dado(dados):
    with open(dados_dado_file, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)

class MeuPrimeiroBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        

    async def setup_hook(self):
        registrar_comandos_ranking(self.tree)
        registrar_comando_dado(self.tree)
        registrar_comando_soma(self.tree)
        registrar_comando_jogo(self.tree, self)
        registrar_comando_adicionar_pergunta(self.tree)
        await self.tree.sync()

    async def on_ready(self):
        print(f"O Bot {self.user} foi ligado com sucesso.")

bot = MeuPrimeiroBot()

# Inicia o bot
bot.run(TOKEN_DISCORD)
