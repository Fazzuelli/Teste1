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

TOKEN_DISCORD = keys.get("token")

# Arquivo de ranking
ranking_file = "commands/ranking.json"

def carregar_ranking():
    if os.path.exists(ranking_file):
        with open(ranking_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_ranking(ranking):
    with open(ranking_file, "w", encoding="utf-8") as f:
        json.dump(ranking, f, indent=4)

 # Arquivo de dados do dado
dados_dado_file = "commands/dados_maximos.json"

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
        registrar_comandos_ranking(self.tree)
        registrar_comando_dado(self.tree)
        registrar_comando_soma(self.tree)
        registrar_comando_jogo(self.tree, self)
        await self.tree.sync()

    async def on_ready(self):
        print(f"O Bot {self.user} foi ligado com sucesso.")

bot = MeuPrimeiroBot()

# Comando: /olá-mundo
@bot.tree.command(name="olá-mundo", description="Primeiro comando do Bot")
async def olamundo(interaction: discord.Interaction):
    await interaction.response.send_message(f"Olá {interaction.user.mention}!")

# Comando: /dado
@bot.tree.command(name="dado", description="Rola um dado com número de lados definido")
@app_commands.describe(lados="Número de lados do dado (ex: 6 para um dado comum)")
async def rolar_dado(interaction: discord.Interaction, lados: int):
    if lados < 1:
        await interaction.response.send_message("O número de lados deve ser maior que zero.")
        return

    resultado = random.randint(1, lados)

    # Carrega e atualiza o maior valor
    dados = carregar_dados_dado()
    user_id = str(interaction.user.id)
    username = interaction.user.display_name

    if user_id not in dados or resultado > dados[user_id]["maior_valor"]:
        dados[user_id] = {"nome": username, "maior_valor": resultado}
        salvar_dados_dado(dados)

    await interaction.response.send_message(
        f"🎲 Você rolou um dado de {lados} lados e tirou **{resultado}**!"
    )
# Comando: /soma
@bot.tree.command(name="soma", description="Soma dois números inteiros")
@app_commands.describe(numero1="Primeiro número a somar", numero2="Segundo número a somar")
async def somar(interaction: discord.Interaction, numero1: int, numero2: int):
    resultado = numero1 + numero2
    await interaction.response.send_message(f"A soma de {numero1} + {numero2} é **{resultado}**.", ephemeral=True)

# Comando: /jogo-de-perguntas
@bot.tree.command(name="jogo-de-perguntas", description="Jogo de perguntas e respostas")
async def jogo_de_perguntas(interaction: discord.Interaction):
    perguntas_respostas = perguntas.perguntas_respostas

    pergunta, resposta = random.choice(perguntas_respostas)
    await interaction.response.send_message(f"🎓 Pergunta: {pergunta}\nResponda no chat em até 30 segundos...")

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        if msg.content.strip().lower() == resposta:
            ranking = carregar_ranking()
            user_id = str(interaction.user.id)
            username = interaction.user.display_name

            if user_id in ranking:
                ranking[user_id]["pontos"] += 1
            else:
                ranking[user_id] = {"nome": username, "pontos": 1}

            salvar_ranking(ranking)
            await interaction.followup.send(f"✅ Resposta correta, {interaction.user.mention}! Agora você tem {ranking[user_id]['pontos']} ponto(s).")
        else:
            await interaction.followup.send(f"❌ Resposta errada, {interaction.user.mention}! A resposta certa era: **{resposta.capitalize()}**.")
    except:
        await interaction.followup.send(f"⏰ {interaction.user.mention}, você não respondeu a tempo!")




# Inicia o bot
bot.run(TOKEN_DISCORD)
