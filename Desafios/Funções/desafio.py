def menu():
    menu = """
    [0] Depositar
    [1] Sacar
    [2] Extrato
    [3] Nova Conta
    [4] Listar Contas
    [5] Novo Usuário
    [6] Sair
    """
    return int(input(menu))


def depositar(valor, saldo, extrato):
    if valor >= 0:
        saldo = saldo + valor
        extrato = f"Depositado: R${saldo}"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("Valores Negativos não são aceitos, favor retornar a operação ")

    return saldo, extrato


def sacar(*, valor, saldo, extrato, saqueDiario, limiteDeSaque, limite):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saque = saqueDiario >= limiteDeSaque

    if excedeu_saldo:
        print("\n Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("\n Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saque:
        print("\n@@@ Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo = saldo - valor
        extrato = saldo
        saqueDiario = saqueDiario + 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n Operação falhou! O valor informado é inválido. ")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:R$ {saldo:.2f}")
    print("==========================================")


def cadastro_usuario(usuarios):
    cpf = int(input("Informe o CPF (Somente números): "))
    usuario = filtro(cpf, usuarios)
    print(usuario)

    if usuario:
        print('Já existe usúario com esse CPF')
        return

    nome = str(input("Informe o nome completo: "))
    data_Nascimento = str(input("Informe a data de nascimento (dd-mm-aaaa)"))
    endereço = str(input("Informe o endereço (logradouro, nro - bairro - cidade/sigra estado): "))
    usuarios.append({"nome": nome, "data_nascimento": data_Nascimento, "endereço": endereço, "CPF": cpf})
    print("usuário criado com sucesso!!")



def filtro(cpf, usuarios):
    for usuario in usuarios:
        if usuario["CPF"] == cpf:
            return usuario
        else:
            return None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = int(input("Informe o CPF do usuário: "))
    usuario = filtro(cpf, usuarios)

    if usuario:
        print( "Conta criada com sucesso! ")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("Usuário não encontrado, fluxo de criação de conta encerrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:{conta['agencia']}
            C/C:{conta['numero_conta']}
            Titular:{conta["usuario"]['nome']} 
        """
        print("=" * 100)
        print((linha))


def main():
    AGENCIA = "0001"
    LIMITEDESAQUE = 3

    saldo = 0
    saqueDiario = 0
    limite = 500
    extrato = 0
    usuarios = list()
    contas = list()

    while True:

        opção = menu()

        if opção == 0:
            valor = float(input("Qual valor deseja depositar R$ "))
            saldo, extrato = depositar(valor, saldo, extrato)

        elif opção == 1:
            valor = float(input("Qual o valor deseja sacar R$ "))
            saldo, extrato = sacar(
                valor=valor,
                saldo=saldo,
                extrato=extrato,
                saqueDiario=saqueDiario,

                limiteDeSaque=LIMITEDESAQUE,
                limite=limite
            )

        elif opção == 2:
            exibir_extrato(saldo, extrato=extrato)

        elif opção == 3:
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opção == 4:
            listar_contas(contas)

        elif opção == 5:
            cadastro_usuario(usuarios)

        elif opção == 6:
            print("Saindo da operação")
            break
        else:
            print("Operação inválida, Tente outra vez")


main()

print(f'Operação finalizada')
