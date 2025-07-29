import discord
from discord import app_commands
import random


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
@app_commands.describe(
    lados="Número de lados do dado (ex: 6 para um dado comum)"
)
async def rolar_dado(interaction: discord.Interaction, lados: int):
    if lados < 1:
        await interaction.response.send_message("O número de lados deve ser maior que zero.")
    else:
        resultado = random.randint(1, lados)
        await interaction.response.send_message(f"🎲 Você rolou um dado de {lados} lados e tirou **{resultado}**!")

# Comando: /soma
@bot.tree.command(name="soma", description="Soma dois números inteiros")
@app_commands.describe(
    numero1="Primeiro número a somar",
    numero2="Segundo número a somar"
)
async def somar(interaction: discord.Interaction, numero1: int, numero2: int):
    resultado = numero1 + numero2
    await interaction.response.send_message(f"A soma de {numero1} + {numero2} é **{resultado}**.", ephemeral=True)

# Comando: /jogo-de-perguntas
@bot.tree.command(name="jogo-de-perguntas", description="Jogo de perguntas e respostas")
async def jogo_de_perguntas(interaction: discord.Interaction):
    perguntas_respostas = [
        ("Qual a capital da França?", "paris"),
        ("Qual é o maior planeta do sistema solar?", "júpiter"),
        ("Quem escreveu 'Dom Casmurro'?", "machado de assis"),
        ("Qual é a fórmula da água?", "h2o"),
        # ... (adicione mais perguntas se quiser)
    ]

    pergunta, resposta_correta = random.choice(perguntas_respostas)
    await interaction.response.send_message(f"🎓 Pergunta: {pergunta}\nResponda no chat em até 30 segundos...")

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        if msg.content.strip().lower() == resposta_correta:
            await interaction.followup.send(f"✅ Resposta correta, {interaction.user.mention}!")
        else:
            await interaction.followup.send(f"❌ Resposta errada, {interaction.user.mention}! A resposta certa era: **{resposta_correta.capitalize()}**.")
    except:
        await interaction.followup.send(f"⏰ {interaction.user.mention}, você não respondeu a tempo!")

# Executa o bot
import token_1
discord_token = token_1.discord_token
bot.run("discord_token")