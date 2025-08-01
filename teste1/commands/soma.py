# commands/soma.py
from discord import app_commands, Interaction

def registrar_comando_soma(tree: app_commands.CommandTree):
    @tree.command(name="soma", description="Soma dois números inteiros")
    @app_commands.describe(numero1="Primeiro número", numero2="Segundo número")
    async def somar(interaction: Interaction, numero1: int, numero2: int):
        resultado = numero1 + numero2
        await interaction.response.send_message(f"A soma de {numero1} + {numero2} é **{resultado}**.")
