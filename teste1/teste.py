import json

# Caminho do arquivo
arquivo = "dados.json"

# Carrega os dados existentes (ou cria estrutura vazia se o arquivo estiver vazio)
try:
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    dados = {"usuarios": []}

# Novo item a ser inserido
novo_usuario = {
    "nome": input("Digite o nome do usuário: "),
    "idade": int(input("Digite a idade do usuário: ")),
}

# Adiciona o item à lista
dados["usuarios"].append(novo_usuario)

# Salva de volta no arquivo
with open(arquivo, "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=4, ensure_ascii=False)

print("Usuário adicionado com sucesso!")
