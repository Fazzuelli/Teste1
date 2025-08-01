# commands/jogo.py
from discord import app_commands, Interaction
import random
import json
import os
from commands.perguntas import perguntas_respostas

ranking_file = "commands/ranking.json"

def carregar_ranking():
    if os.path.exists(ranking_file):
        with open(ranking_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_ranking(ranking):
    with open(ranking_file, "w", encoding="utf-8") as f:
        json.dump(ranking, f, indent=4)

def registrar_comando_jogo(tree: app_commands.CommandTree, bot):
    @tree.command(name="jogo-de-perguntas", description="Jogo de perguntas e respostas")
    async def jogo_de_perguntas(interaction: Interaction):
        pergunta, resposta = random.choice(perguntas_respostas)
        await interaction.response.send_message(f"🎓 Pergunta: {pergunta}\nResponda no chat em até 30 segundos...")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.strip().lower() == resposta.lower():
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
                await interaction.followup.send(f"❌ Resposta errada! A resposta certa era: **{resposta}**.")
        except:
            await interaction.followup.send(f"⏰ Você não respondeu a tempo!")
