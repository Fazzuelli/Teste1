from discord import app_commands, Interaction
from commands.perguntas import carregar_perguntas, salvar_perguntas

def registrar_comando_adicionar_pergunta(tree: app_commands.CommandTree):
    @tree.command(name="adicionar-pergunta", description="Adiciona uma nova pergunta e resposta ao jogo")
    @app_commands.describe(pergunta="Digite a pergunta", resposta="Digite a resposta correta")
    async def adicionar_pergunta(interaction: Interaction, pergunta: str, resposta: str):
        perguntas = carregar_perguntas()

        nova = {"pergunta": pergunta, "resposta": resposta}
        perguntas.append(nova)
        salvar_perguntas(perguntas)

        await interaction.response.send_message("✅ Pergunta registrada com sucesso!", ephemeral=True)