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

TOKEN_DISCORD = keys.get("token")
listModels = []

# Arquivo de ranking
ranking_file = "ranking.json"

def carregar_ranking():
    if os.path.exists(ranking_file):
        with open(ranking_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_ranking(ranking):
    with open(ranking_file, "w", encoding="utf-8") as f:
        json.dump(ranking, f, indent=4)

 # Arquivo de dados do dado
dados_dado_file = "dados_maximos.json"

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

# Comando: /ranking
@bot.tree.command(name="ranking", description="Mostra o ranking dos jogadores com mais acertos")
async def ranking(interaction: discord.Interaction):
    ranking = carregar_ranking()

    if not ranking:
        await interaction.response.send_message("📊 Ainda não há jogadores no ranking.")
        return

    ranking_ordenado = sorted(ranking.items(), key=lambda item: item[1]["pontos"], reverse=True)

    mensagem = "🏆 **Ranking dos melhores jogadores:**\n\n"
    for i, (user_id, dados) in enumerate(ranking_ordenado[:5], start=1):
        mensagem += f"{i}. **{dados['nome']}** – {dados['pontos']} ponto(s)\n"

    await interaction.response.send_message(mensagem)

# Comando: /ranking-dados
@bot.tree.command(name="ranking-dados", description="Mostra quem já tirou os maiores valores no dado")
async def ranking_dados(interaction: discord.Interaction):
    dados = carregar_dados_dado()

    if not dados:
        await interaction.response.send_message("📊 Ainda não há dados registrados de rolagens.")
        return

    dados_ordenados = sorted(dados.items(), key=lambda item: item[1]["maior_valor"], reverse=True)

    mensagem = "🎯 **Maiores valores já tirados no dado:**\n\n"
    for i, (user_id, info) in enumerate(dados_ordenados[:5], start=1):
        mensagem += f"{i}. **{info['nome']}** – {info['maior_valor']}\n"

    await interaction.response.send_message(mensagem)


import google.generativeai as genai

# Configurar a API do Gemini
genai.configure(api_key=keys.get("gemini_api_key"))  # Supondo que você salvou no arquivo keys.py

@bot.tree.command(name="pergunte", description="Pergunte algo para a IA do Google Gemini")
@app_commands.describe(pergunta="Sua pergunta para a IA")
async def pergunte(interaction: discord.Interaction, pergunta: str):
    await interaction.response.defer()

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(pergunta)
        texto = response.text.strip()

        if not texto:
            texto = "🤖 A IA não conseguiu gerar uma resposta útil para isso."

        await interaction.followup.send(f"🤖 {texto}")

    except Exception as e:
        print("Erro ao consultar Gemini:", e)
        await interaction.followup.send("❌ Erro ao consultar o Gemini. Verifique sua chave ou limite de uso.")




# Inicia o bot
bot.run(TOKEN_DISCORD)
