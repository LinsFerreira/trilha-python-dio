''' 
Desafio Otimizando o Sistema Bancário com Python
Por Walterlins Ferreira
'''
# Este módulo faz quebra automática de linha e faz alinhamento dos textos.
import textwrap

def menu():
 
    menu = """\n
    --------------- MENU ----------------
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova Conta
    [nu] Novo Usuário
    [lc] Lista Contas
    [q] Sair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):    
    # Tudo que estiver antes do /, significa que or argumentos devem ser passados por posição.
    
        if valor > 0:
            saldo += valor
            extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== \033[32mDepósito realizado com sucesso! \033[0m")
        else:
            print("\n\033[31m Operação falhou! O valor informado é inválido. \033[0m")
        
        return saldo, extrato
            
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    # O que vem depois do *, indica que esta recebendo os argumentos de forma nomeada.

        excedeu_saldo  = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= limite_saques
        
        if excedeu_saldo:
            print("\n\033[31m Operação falhou! Você não tem saldo suficiente. \033[0m")

        elif excedeu_limite:
            print("\n\033[31m Operação falhou! O valor do saque excede o limite. \033[0m")

        elif excedeu_saques:
            print("\n\033[31m Operação falhou! Número máximo de saques excedido. \033[0m")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print("\n\033[32m Saque realizado com sucesso! \033[0m")
        else:
            print("\033[31m Operação falhou! O valor informado é inválido. \033m[0m")
            
        return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    # Recebe os argumentos de forma posicional e nomeada.
    
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\n\tSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf     = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\n \033[31m Já existe usuário com esse CPF! \033[0m")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (Logradouro, nro - bairro - cidade/sigla estado): ")
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco })
    
    print("\033[32m Usuário criado com sucesso! \033[0m")

def filtrar_usuario(cpf, usuarios):
    # Realizamos uma compressão de listas
    
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf ]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    
    cpf     = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\n \033[32m Conta criada com sucesso! \033[0m")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n \033[31mUsuário não encontrado, fluxo de criação da conta encerrado! \033[0m")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))
        
def main():
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = '0001'
    usuarios= []
    contas = []

    while True:

        opcao = menu()
        
        if opcao == "d":
            valor = input("Informe o valor do depósito: ")
            
            if valor == '':
                print("\033[31mO valor do depósito é obrigatório!\033[0m")
                continue
            else:
                valor = float(valor)
            
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = input("Informe o valor do saque: ")
            
            if valor == '':
                print("\033[31mO valor do saque é obrigatório!\033[0m")
                continue
            else:           
                valor = float(valor)
        
            saldo,extrato = sacar(
                saldo   = saldo,
                valor   = valor,
                extrato = extrato,
                limite  = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES,
            )
            
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato) # Passando os argumentos de forma posicional e nomeada

        elif opcao == "nu":
            criar_usuario(usuarios)
            
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            
            if conta:
                contas.append(conta)
                
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
