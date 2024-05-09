def faz_deposito(saldo, extrato, /):
    valor = float(input("Qual o valor do seu depósito? "))

    if valor > 0:
        saldo += valor
        extrato += f"+ R$ {valor:.2f}\n"
        mensagem = f"Depósito realizado com sucesso. Saldo: R$ {saldo:.2f}"

    else:
        # print("Por favor, informe um valor maior que 0.")
        mensagem = "Por favor, informe um valor maior que 0."

    return mensagem, saldo, extrato


def faz_saque(*, saldo, extrato, limite, numero_saques, limite_saques):
    valor = float(input("Quando você deseja sacar? "))

    if valor > saldo:
        mensagem = "Você não tem saldo suficiente para fazer esse saque. Por favor, verifique se você tem saldo."

    elif valor > limite:
        mensagem = ("Não foi possível fazer o saque pois o valor excede o limite da transação. Por favor, "
                    "escolha outro valor.")

    elif numero_saques >= limite_saques:
        mensagem = "Você excedeu a quantidade diária de saques permitida. Por favor, tente novamente amanhã."

    elif valor > 0:
        saldo -= valor
        extrato += f"- R$ {valor:.2f}\n"
        numero_saques += 1
        mensagem = f"Saque realizado com sucesso. Saldo: R$ {saldo:.2f}"

    else:
        mensagem = "Por favor, informe um valor maior que 0."

    return mensagem, saldo, extrato, numero_saques


def mostra_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    mensagem_extrato = f"Veja abaixo as suas movimentações:\n\n{extrato}"
    print("Sem movimentações até o momento." if not extrato else mensagem_extrato)
    print(f"Você possui R$ {saldo:.2f} de saldo em sua conta.")
    print("==========================================")


def criar_usuario(usuarios):
    def mostra_usuario(novo_usuario):

        lista = [f" - {chave}: {valor}" for chave, valor in novo_usuario.items()]
        return "\n".join(lista)

    cpf = input("CPF: ")
    if cpf in usuarios:
        return "CPF já cadastrado"

    nome = input("Nome: ")
    data_nascimento = input("Data de Nascimento: ")
    logradouro = input("Logradouro: ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    uf = input("Sigla do Estado: ")

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{uf}"
    cpf = cpf.replace(".", "").replace("-", "")

    novo_usuario = {'nome': nome,
                    'data_nascimento': data_nascimento,
                    'cpf': cpf,
                    'endereco': endereco}

    usuarios[cpf] = novo_usuario

    mensagem = f"Usuário cadastrado com sucesso\n{mostra_usuario(novo_usuario)}"
    return mensagem


def criar_conta(contas, ultima_conta):
    def mostra_conta(nova_conta):

        lista = [f" - {chave}: {valor}" for chave, valor in nova_conta.items()]
        return "\n".join(lista)

    cpf = input("CPF: ")
    if cpf not in usuarios:
        return "CPF não cadastrado", ultima_conta

    agencia = input("Agencia: ")
    ultima_conta += 1

    nova_conta = {'agencia': agencia,
                  'conta': ultima_conta,
                  'usuario': cpf}

    contas[ultima_conta] = nova_conta

    mensagem = f"Conta cadastrada com sucesso\n{mostra_conta(nova_conta)}"

    return mensagem, ultima_conta


def listar_usuarios(usuarios):
    for usuario, dados in usuarios.items():
        print(f"{usuario}: {dados['nome']}")


def listar_contas(contas, usuarios):
    for conta, dados in contas.items():
        cpf = dados['usuario']
        print(f"{conta}: {cpf} ({usuarios[cpf]['nome']})")


mensagem = ""

menu = f"""
Você está no XYZ

[d]  Depositar
[s]  Sacar
[e]  Extrato
-----------------
[u]  Criar usuário
[c]  Criar conta
[lu] Listar usuários
[lc] Lista contas
-----------------
[q]  Sair
"""

LIMITE_POR_SAQUE = 500
LIMITE_SAQUES = 3

extrato = ""
saldo = 0
numero_saques = 0
ultima_conta = 0
usuarios = {}
contas = {}

while True:
    opcao = input(f"{menu}{mensagem}\n=> ")

    mensagem = ""
    if opcao == "d":
        mensagem, saldo, extrato = faz_deposito(saldo, extrato)
    elif opcao == "s":
        mensagem, saldo, extrato, numero_saques = faz_saque(saldo=saldo, extrato=extrato, limite=LIMITE_POR_SAQUE,
                                                            numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
    elif opcao == "e":
        mostra_extrato(saldo, extrato=extrato)
    elif opcao == "u":
        mensagem = criar_usuario(usuarios)
    elif opcao == "c":
        mensagem, ultima_conta = criar_conta(contas, ultima_conta)
    elif opcao == "lu":
        listar_usuarios(usuarios)
    elif opcao == "lc":
        listar_contas(contas, usuarios)
    elif opcao == "q":
        break
    else:
        mensagem = "Operação não reconhecida. Por favor selecione uma das opções acima."
