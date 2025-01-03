import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(nome, cpf, endereco)
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        if valor > saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False

        if numero_saques >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""
            Agência: {self.agencia}
            C/C: {self.numero}
            Titular: {self.cliente.nome}
            Saldo: R$ {self.saldo:.2f}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
        })


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu():
    return input(textwrap.dedent("""
        ================ MENU ================
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nc] Nova conta
        [lc] Listar contas
        [nu] Novo usuário
        [q] Sair
        => """))


def filtrar_cliente(cpf, clientes):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]


def realizar_transacao(clientes, tipo_transacao):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input(f"Informe o valor do {tipo_transacao}: "))
    transacao = Deposito(valor) if tipo_transacao == 'depósito' else Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        print("\n================ EXTRATO ================")
        transacoes = conta.historico.transacoes
        if not transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in transacoes:
                print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f} em {transacao['data']}")
        print(f"\nSaldo: R$ {conta.saldo:.2f}")
        print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.adicionar_conta(conta)
        print("\n=== Conta criada com sucesso! ===")
    else:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    if not contas:
        print("\n@@@ Não há contas para listar! @@@")
        return
    for conta in contas:
        print("=" * 100)
        print(conta)


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            realizar_transacao(clientes, 'depósito')

        elif opcao == "s":
            realizar_transacao(clientes, 'saque')

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()
