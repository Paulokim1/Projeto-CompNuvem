#App 
from time import sleep
import os

def show_welcome():
    msg = """
=================================== BEM-VINDO ===================================
Esta aplicação foi desenvolvida com o intuito de provisionar uma instância EC2 na AWS
por meio do terminal de uma maneira simples, fácil e amigável. Aqui, você poderá
gerenciá-la e adminstrá-la (construir e deletar recursos) de maneira intuitiva. 

Antes de começar, é necessário que você selecione uma região.
"""
    print(msg)

    msg = """
1 - US East (N. Virginia)

2 - US East (Ohio)

3 - Sair

"""
    sleep(1.5)
    print(msg)

    ans = input("Digite a opção desejada: ")

    if ans == "1":
        print("\033[1;32mVocê selecionou US East (N. Virginia)" + "\033[0m")
        sleep(1)
        ans_2 = input("Você confirma? (s/n): ")
        if ans_2 == "s":
            os.system("cd users && terraform init")
            os.system("clear")
            os.system("cd us-east-1 && python main.py")
        elif ans_2 == "n":
            return

    elif ans == "2":
        print("\033[1;32mVocê selecionou US East (Ohio)" + "\033[0m")
        sleep(1)
        ans_2 = input("Você confirma? (s/n): ")
        if ans_2 == "s":
            os.system("cd users && terraform init")
            os.system("clear")
            os.system("cd us-east-2 && python main.py")
        elif ans_2 == "n":
            return

    return -1

def main():
    RUNNING = True

    while RUNNING:
        app = show_welcome()
        if app == -1:
            print("\033[1;31mEncerrando a aplicação...." + "\033[0m")
            sleep(2)
            RUNNING = False


if __name__ == "__main__":
    main()



