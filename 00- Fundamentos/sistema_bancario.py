# Criando as Variáveis
saldo = 0
saque_diario = 0
limite = 500
saque_maximo = 3
extrato = ""

menu = """
[0] Depositar
[1] Sacar
[2] Extrato
[3] Sair
"""

while True:
    opcao = int(input(menu))
    if opcao == 0:
        valor = float(input('Qual valor deseja depositar R$'))
        if valor >=0:
            saldo = saldo + valor
            extrato = f'Depositado: R${saldo}'
            print("Depositado....")
        else:
            print('Valores negativos não são aceitos, por favor volte a transação...')
    
    
    elif opcao == 1:
        valor = float(input("Qual o valor que deseja sacar R$ "))
        if saque_diario <= 2 and valor <= saldo and valor <= 500:
            saldo = saldo - valor
            extrato = saldo 
            saque_diario = saque_diario + 1

        elif valor > 500:
            print("O valor máximo de retirada é de R$ 500, apartir desse valor não poderá ser realizado a operação!!")

        elif valor > saldo:
            print("O valor é maior que o saldo da conta, favor refazer a operação!")

        else:
            print("limite de saque diário esgotado!!! ")

    elif opcao == 2:
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == 3:
        print('Saindo da operação')
        break

    else:
        print("Operação inválida, Tente outra vez")

print('Operação Finalizada!')
