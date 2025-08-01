from discord import app_commands, Interaction
import json
import os

# Caminhos corretos
ranking_file = "commands/ranking.json"
dados_dado_file = "commands/dados_maximos.json"

# Funções auxiliares
def carregar_ranking():
    if os.path.exists(ranking_file):
        with open(ranking_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def carregar_dados_dado():
    if os.path.exists(dados_dado_file):
        with open(dados_dado_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Função para registrar o comando
def registrar_comandos_ranking(tree: app_commands.CommandTree):
    @tree.command(name="ranking", description="Mostra o ranking dos jogadores")
    @app_commands.describe(escolha="Escolha o ranking a ser exibido")
    @app_commands.choices(
        escolha=[
            app_commands.Choice(name="Ranking Geral", value="geral"),
            app_commands.Choice(name="Ranking de Dados", value="dados"),
        ]
    )
    async def ranking(interaction: Interaction, escolha: str):
        ranking = carregar_ranking()
        dados = carregar_dados_dado()

        if escolha == "dados":
            if not dados:
                await interaction.response.send_message("📊 Ainda não há dados registrados de rolagens.")
                return

            dados_ordenados = sorted(dados.items(), key=lambda item: item[1]["maior_valor"], reverse=True)

            mensagem = "🎯 **Maiores valores já tirados no dado:**\n\n"
            for i, (user_id, info) in enumerate(dados_ordenados[:5], start=1):
                mensagem += f"{i}. **{info['nome']}** – {info['maior_valor']}\n"

            await interaction.response.send_message(mensagem)
            return

        if not ranking:
            await interaction.response.send_message("📊 Ainda não há jogadores no ranking.")
            return

        ranking_ordenado = sorted(ranking.items(), key=lambda item: item[1]["pontos"], reverse=True)

        mensagem = "🏆 **Ranking dos melhores jogadores:**\n\n"
        for i, (user_id, dados) in enumerate(ranking_ordenado[:5], start=1):
            mensagem += f"{i}. **{dados['nome']}** – {dados['pontos']} ponto(s)\n"

        await interaction.response.send_message(mensagem)
