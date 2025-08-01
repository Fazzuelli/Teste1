# commands/dado.py
from discord import app_commands, Interaction
import random
import json
import os

dados_dado_file = "commands/dados_maximos.json"

def carregar_dados_dado():
    if os.path.exists(dados_dado_file):
        with open(dados_dado_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_dados_dado(dados):
    with open(dados_dado_file, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)

def registrar_comando_dado(tree: app_commands.CommandTree):
    @tree.command(name="dado", description="Rola um dado com número de lados definido")
    @app_commands.describe(lados="Número de lados do dado (ex: 6 para um dado comum)")
    async def rolar_dado(interaction: Interaction, lados: int):
        if lados < 1:
            await interaction.response.send_message("O número de lados deve ser maior que zero.")
            return

        resultado = random.randint(1, lados)
        user_id = str(interaction.user.id)
        username = interaction.user.display_name

        dados = carregar_dados_dado()
        if user_id not in dados or resultado > dados[user_id]["maior_valor"]:
            dados[user_id] = {"nome": username, "maior_valor": resultado}
            salvar_dados_dado(dados)

        await interaction.response.send_message(
            f"🎲 Você rolou um dado de {lados} lados e tirou **{resultado}**!"
        )
