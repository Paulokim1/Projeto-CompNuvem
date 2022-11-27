# Imports 
from time import sleep
import os
import json
import re

# State variables
COMMAND = {

    "CREATE" : 1,
    "DELETE" : 2, 
    "EDIT" : 3
}

FIRST_TIME = True
RUNNING = True

def print_ask_question():
    while True:
        try:
            menu_ans = int(input("Digite o número da opção desejada: "))
            break   
        except ValueError:
            print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
            print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
    return menu_ans


# Display functions
def show_welcome():
    msg = """
=================================== BEM-VINDO ===================================
Esta aplicação foi desenvolvida com o intuito de provisionar uma instância EC2 na AWS
por meio do terminal de uma maneira simples, fácil e amigável. Aqui, você poderá
gerenciá-la e adminstrá-la (construir e deletar recursos) de maneira intuitiva. 

Vamos iniciar o Terraform para você, aguarde um instante...

    """
    print(msg)
    sleep(1)
    os.system('terraform init')

def show_menu():
    if not FIRST_TIME:
        os.system("clear")
    menu = """
============================ TERRAFORM EC2 MENU ===================================
Selecione o comando desejado:

1. Criar 

2. Deletar

3. Listar

4. Sair

    """
    print(menu)
    
    menu_ans = print_ask_question()
            

    while menu_ans not in [1,2,3,4]:
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        menu_ans = print_ask_question()

    if menu_ans == 1:
        show_create_menu()
    elif menu_ans == 2:
        show_delete_menu()
    elif menu_ans == 3:
        show_list_menu()
    else:
        global RUNNING
        RUNNING = False
        print("\033[1;31mExit indentificado!" + "\033[0m")
        sleep(1)

    return



def show_create_menu():
    os.system("clear")
    menu = """
================================ CREATE MENU =======================================
Selecione o comando desejado:

1. Criar instância

2. Criar security group

3. Criar usuário

4. Voltar p/ menu principal

    """
    print(menu)

    menu_ans = print_ask_question()

    while menu_ans not in [1,2,3,4]:
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        menu_ans = print_ask_question()

    if menu_ans == 1: 
        show_create_menu_option_1()
    elif menu_ans == 2: 
        show_create_menu_option_2()
    elif menu_ans == 3:
        show_create_menu_option_3()
    else:
        return    

def show_create_menu_option_1():
    data_to_json = {
        "name": "",
        "ami": "",
        "instance_type": "", 
        "sg-name": ""
    }

    os.system("clear")
    ami_name = ""

    # Definição do NAME
    menu = """
============================ CREATE INSTÂNCIA: Nome da instância ==========================
Como você deseja nomear sua instância?

    """
    print(menu)

    instance_name = input("Digite o nome aqui: ")
    data_to_json["name"] = instance_name


    # Definição do AMI
    os.system("clear")
    menu = """
============================ CREATE INSTÂNCIA: AMI =======================================
Selecione o AMI desejado:

1. Ubuntu Server 18.04 LTS 

2. Ubuntu Server 20.04 LTS 

3. Ubuntu Server 22.04 LTS 

4. Cancelar

    """
    print(menu)

    menu_ans = print_ask_question()

    while menu_ans not in [1,2,3,4]:
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        menu_ans = print_ask_question()

    if menu_ans == 1:
        data_to_json["ami"] = "ami-0ee23bfc74a881de5"
        ami_name = "Ubuntu Server 18.04 LTS"
    
    elif menu_ans == 2:
        data_to_json["ami"] = "ami-0149b2da6ceec4bb0"
        ami_name = "Ubuntu Server 20.04 LTS "

    elif menu_ans == 3:
        data_to_json["ami"] = "ami-08c40ec9ead489470"
        ami_name = "Ubuntu Server 22.04 LTS "

    else:
        return
    

    # Definição do INSTANCE_TYPE
    os.system("clear")
    menu = """
============================ CREATE INSTÂNCIA: Tipo de instância ============================
Selecione o tipo de instância desejada:

1. t2.micro

2. t2.small

3. t2.medium

4. t2.large

5. Cancelar

    """
    print(menu)

    menu_ans = print_ask_question()

    while menu_ans not in [1,2,3,4,5]:
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        menu_ans = print_ask_question()

    if menu_ans == 1:
        data_to_json["instance_type"] = "t2.micro"
    
    elif menu_ans == 2:
        data_to_json["instance_type"] = "t2.small"

    elif menu_ans == 3:
        data_to_json["instance_type"] = "t2.medium"

    elif menu_ans == 4:
        data_to_json["instance_type"] = "t2.large"

    else:
        return

    # Definição do security group
    os.system("clear")
    menu = """
============================ CREATE INSTÂNCIA: Security Group ============================
Qual secuity group você deseja associar a sua instância?:

    """
    print(menu)
    count = 0
    for sg in security_groups_list:
        print(f"{count+1}. {sg}\n")
        count += 1

    menu_ans = print_ask_question()
    while menu_ans not in range(1, len(security_groups_list)+1):
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        menu_ans = print_ask_question()
        
    data_to_json["sg-name"] = security_groups_list[menu_ans-1]

    # Checagem
    with open(".auto.tfvars.json", 'r+') as f:
        data = json.load(f)
        chosen_sg = data["security_groups"][menu_ans-1]
    os.system("clear")
    menu = """
============================ CREATE INSTÂNCIA: Checagem =====================================
A configuração da sua instância ficou da seguinte maneira:
    """
    print(menu)
    print(f'Nome da instância: {data_to_json["name"]}\n')
    print(f'AMI: {ami_name}\n')
    print(f'Tipo: {data_to_json["instance_type"]}\n')
    print(f'Security Group:\n')
    print(f'    Nome: {chosen_sg["name"]}\n')
    print(f'    Regras:\n')
    count = 1
    for rule in chosen_sg["ingress"]:
        print(f'        {count}.')
        print(f'        Porta (from): {rule["from_port"]}')
        print(f'        Porta (to): {rule["to_port"]}')
        print(f'        Protocolo: {rule["protocol"]}')
        print(f'        IP de origem: {rule["cidr_blocks"]}\n')
        count += 1
    ans = input("Você confirma esses dados? [s/n]: ")

    if ans == "s":
        instance_list.append(instance_name)
        with open(".auto.tfvars.json", 'r+') as f:
            data = json.load(f)
            data["instances"].append(data_to_json)
            f.seek(0) 
            json.dump(data,f, indent=4)
            f.truncate()
        print("\033[1;32mInstância sendo criado em instantes, aguarde ..." + "\033[0m")
        sleep(1.5)
        os.system("clear & terraform apply  --auto-approve")
        print("\033[1;32mInstância criada com sucesso!" + "\033[0m")
        sleep(4)
        return

    else:
        print("\033[1;31mInstância não criada." + "\033[0m")
        sleep(4)
        return

def show_create_menu_option_2():
    sg_to_json = {
        "name": "",
        "ingress": []
    }

    # From port
    os.system("clear")
    menu = """
============================ CREATE SECURITY GROUP: Nome ============================
    """
    print(menu)

    sg_name = input("Qual será o nome do seu security group?: ")
    sg_to_json["name"] = sg_name


    # Quantas regras de ingresso?
    os.system("clear")
    menu = """
============================ CREATE SECURITY GROUP: Quantidade de regras ============================
    """
    print(menu)

    num_rules = int(input("Quantas regras de ingresso você deseja adicionar?: "))
    while num_rules not in range(1, 11):
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        num_rules = int(input("Quantas regras de ingresso você deseja adicionar?: "))

    rules = 0
    while rules < num_rules:
        ingress = {
            "from_port": "",
            "to_port": "",
            "protocol": "",
            "cidr_blocks": []
        }

        # From port
        os.system("clear")
        print(f"\033[1;32mRegra: {rules+1}" + "\033[0m\n")
        menu = """
============================ CREATE SECURITY GROUP: from_port ============================
        """
        print(menu)

        menu_ans = int(input("A partir de qual porta você deseja criar? (from_port): "))

        while menu_ans not in range(1, 65535):
            print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
            print("Por favor, digite uma porta válida. Tente novamente.")
            menu_ans = int(input("A partir de qual porta você deseja criar? (from_port): "))

        ingress["from_port"] = menu_ans

        # to port
        os.system("clear")
        print(f"\033[1;32mRegra: {rules+1}" + "\033[0m\n")
        menu = """
============================ CREATE SECURITY GROUP: to_port ============================
        """
        print(menu)

        menu_ans = int(input("Até qual porta você deseja criar? (to_port): "))

        while menu_ans not in range(1, 65535):
            print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
            print("Por favor, digite uma porta válida. Tente novamente.")
            menu_ans = int(input("Até qual porta você deseja criar? (to_port): "))

        ingress["to_port"] = menu_ans

        # protocol
        os.system("clear")
        print(f"\033[1;32mRegra: {rules+1}" + "\033[0m\n")
        menu = """
============================ CREATE SECURITY GROUP: protocol ============================

    1. tcp

    2. udp

    3. icmp
        """
        print(menu)

        menu_ans = int(input("Qual protocolo você deseja criar? (protocol): "))

        while menu_ans not in [1,2,3]:
            print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
            print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
            menu_ans = int(input("Qual protocolo você deseja criar? (protocol): "))

        if menu_ans == 1:
            ingress["protocol"] = "tcp"
        elif menu_ans == 2:
            ingress["protocol"] = "udp"
        else:
            ingress["protocol"] = "icmp"

        # cidr_blocks 
        os.system("clear")
        print(f"\033[1;32mRegra: {rules+1}" + "\033[0m\n")
        menu = """
============================ CREATE SECURITY GROUP: cidr_blocks ============================
        """
        print(menu)

        menu_ans = input("Qual CIDR você deseja criar? (cidr_blocks) <Ex: 0.0.0.0/0>: ")

        s = re.sub("\d+", "", menu_ans)
        while s != ".../":
            print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
            print("Por favor, digite um CIDR válido. Tente novamente.")
            menu_ans = input("Qual CIDR você deseja criar? (cidr_blocks) <Ex: 0.0.0.0/0>: ")
            s = re.sub("\d+", "", menu_ans)

        ingress["cidr_blocks"].append(menu_ans)

        sg_to_json["ingress"].append(ingress)
        rules += 1

    

    # Checagem
    os.system("clear")
    menu = """
============================ CREATE SECURITY GROUP: Checagem =====================================
A configuração da sua instância ficou da seguinte maneira:
    """
    print(menu)
    print(f'Nome do security group: {sg_to_json["name"]}\n')

    for i in range(len(sg_to_json["ingress"])):
        print(f"--- Regra {i+1} ---")
        print(f'from_port: {sg_to_json["ingress"][i]["from_port"]}\n')
        print(f'to_port: {sg_to_json["ingress"][i]["to_port"]}\n')
        print(f'protocol: {sg_to_json["ingress"][i]["protocol"]}\n')
        print(f'cidr_blocks: {sg_to_json["ingress"][i]["cidr_blocks"]}\n')
        print("")
    
    ans = input("Você confirma esses dados? [s/n]: ")

    if ans == "s":
        security_groups_list.append(sg_name)
        with open(".auto.tfvars.json", 'r+') as f:
            data = json.load(f)
            data["security_groups"].append(sg_to_json)
            f.seek(0) 
            json.dump(data,f, indent=4)
            f.truncate()
        print("\033[1;32mSecurity Group sendo criado em instantes, aguarde..." + "\033[0m")
        sleep(1.5)
        os.system("clear & terraform apply  --auto-approve")
        print("\033[1;32mSecurity Group criado com sucesso!" + "\033[0m")
        sleep(4)
        return
    
    else:
        print("\033[1;31mSecurity Group não criada" + "\033[0m")
        sleep(4)
        return

def show_create_menu_option_3():
    user_to_json = {
        "name": "",
        "restrictions": {
            "actions": [],
            "resources": []
        }
    }

    os.system("clear")
    menu = """
============================ CREATE USER: Nome ============================
    """
    print(menu)

    user_name = input("Qual será o nome do seu usuário?: ")
    user_to_json["name"] = user_name

    # Restrictions - Actions
    os.system("clear")
    menu = """
============================ CREATE USER: Restrições - Actions ============================
    """
    print(menu)

    menu_ans = input("Qual será a restrição do seu usuário em relação ao ACTIONS?: ")
    user_to_json["restrictions"]["actions"].append(menu_ans)

    # Restrictions - Resources
    os.system("clear")
    menu = """
============================ CREATE USER: Restrições - Resources ============================
    """
    print(menu)

    menu_ans = input("Qual será a restrição do seu usuário em relação ao RESOURCES?: ")
    user_to_json["restrictions"]["resources"].append(menu_ans)

    # Checagem
    os.system("clear")
    menu = """
============================ CREATE USER : Checagem =====================================
A configuração da sua instância ficou da seguinte maneira:
    """
    print(menu)
    print(f'Nome do usuário: {user_to_json["name"]}\n')
    print(f'Restrições - Actions: {user_to_json["restrictions"]["actions"]}\n')
    print(f'Restrições - Resources: {user_to_json["restrictions"]["resources"]}\n')

    ans = input("Você confirma esses dados? [s/n]: ")

    if ans == "s":
        users_list.append(user_name)
        with open("../users/.auto.tfvars.json", 'r+') as f:
            data = json.load(f)
            data["users"].append(user_to_json)
            f.seek(0) 
            json.dump(data,f, indent=4)
            f.truncate()
        print("\033[1;32mUsuário sendo criado em instantes, aguarde..." + "\033[0m")
        sleep(1.5)
        os.system("clear & cd .. && cd users && terraform apply  --auto-approve")
        print("\033[1;32mUsuário criado com sucesso!" + "\033[0m")
        sleep(4)
        return

    else:
        print("\033[1;31mUsuário não criado" + "\033[0m")
        sleep(4)
        return



def show_delete_menu():
    os.system("clear")
    menu = """
================================== DELETE MENU =========================================
Selecione o comando desejado:

1. Deletar instância

2. Deletar security group

3. Deletar regras de um security group

4. Deletar usuário

5. Voltar p/ menu principal

    """
    print(menu)

    menu_ans = int(input("Digite o número da opção desejada: "))

    while menu_ans not in [1,2,3,4,5]:
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        menu_ans = int(input("Digite o número da opção desejada: "))

    if menu_ans == 1:
        show_delete_menu_option_1()
    elif menu_ans == 2:
        show_delete_menu_option_2()
    elif menu_ans == 3:
        show_delete_menu_option_3()
    elif menu_ans == 4:
        show_delete_menu_option_4()
    else:
        return

def show_delete_menu_option_1():
    os.system("clear")
    menu = """
============================ DELETE INSTÂNCIA ============================
Quais das instâncias abaixo você deseja deletar?

    """
    print(menu)

    for i in range(len(instance_list)):
        print(f'{i+1}. {instance_list[i]}\n')
    
    menu_ans = int(input("Digite o número da opção desejada: "))
    while menu_ans not in range(1,len(instance_list)+1):
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        menu_ans = int(input("Digite o número da opção desejada: "))

    os.system("clear")
            
    menu = """
============================ DELETE INSTÂNCIA ============================
    """
    print(menu)
    print(f"Você deseja mesmo deletar a instância {instance_list[menu_ans-1]}?")

    ans = input("[s/n]: ")

    if ans == "s":
        with open(".auto.tfvars.json", 'r+') as f:
            data = json.load(f)
            data["instances"].pop(menu_ans-1)
            f.seek(0) 
            json.dump(data,f, indent=4)
            f.truncate()
        instance_list.pop(menu_ans-1)
    else:
        print("\033[1;31mInstância não deletada" + "\033[0m")
        sleep(4)
        return

    print("\033[1;32mInstância sendo deletada em instantes, aguarde..." + "\033[0m")
    sleep(1.5)
    os.system("clear & terraform apply  --auto-approve")
    print("\033[1;32mInstância deletada com sucesso!" + "\033[0m")
    sleep(4)
    return

def show_delete_menu_option_2():
    os.system("clear")
    menu = """
============================ DELETE SECURITY GROUP ============================
Quais dos security groups abaixo você deseja deletar?

    """
    print(menu)

    for i in range(len(security_groups_list)):
        print(f'{i+1}. {security_groups_list[i]}\n')

    print(f"{len(security_groups_list)+1}. Voltar p/ menu principal\n")

    menu_ans = int(input("Digite o número da opção desejada: "))
    while menu_ans not in range(1,len(security_groups_list)+2):
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        menu_ans = int(input("Digite o número da opção desejada: "))
    if menu_ans == len(security_groups_list)+1:
        return()
    elif security_groups_list[menu_ans-1] == "default":
        print("\033[1;31mNão é possível deletar o security group default!" + "\033[0m\n")
        input("Pressione qualquer tecla para continuar: ")
        return()
    
    os.system("clear")

    with open(".auto.tfvars.json", 'r+') as f:
        data = json.load(f)
        for instance in data["instances"]:
            if instance["sg-name"] == security_groups_list[menu_ans-1]:
                print("\033[1;31mEste security group está sendo utilizado em uma ou mais instância(s)." + "\033[0m")
                print("\033[1;31mDeletá-lo acarretará no enceramento desta(s) própria(s) instância(s) a seguir:\n" + "\033[0m")
                count = 1
                for instance in data["instances"]:
                    if instance["sg-name"] == security_groups_list[menu_ans-1]:
                        print(f"{count}. {instance['name']}\n")
                        count += 1
                print("Deseja mesmo deletar o security group?\n")
                ans = input("[s/n]: ")
                if ans == "s":
                    instances_to_remove = []
                    for instance in data["instances"]:
                        if instance["sg-name"] == security_groups_list[menu_ans-1]:
                            for i in range(len(instance_list)):
                                if instance["name"] == instance_list[i]:
                                    #data["instances"].remove(instance)
                                    instances_to_remove.append(instance)
                                    #instance_list.pop(i)
                                    break
                    for instance in instances_to_remove:
                        data["instances"].remove(instance)
                        instance_list.remove(instance["name"])
                    data["security_groups"].pop(menu_ans-1)
                    f.seek(0) 
                    json.dump(data,f, indent=4)
                    f.truncate()
                    security_groups_list.pop(menu_ans-1)
                    print("\033[1;32mSecurity group e instâncias sendo deletadas em instantes, aguarde..." + "\033[0m")
                    sleep(1.5)
                    os.system("clear & terraform apply  --auto-approve")
                    print("\033[1;32mSecurity group e instâncias deletadas com sucesso!" + "\033[0m")
                    sleep(4)
                    return()
                else:
                    print("\033[1;31mSecurity group não deletado" + "\033[0m")
                    sleep(4)
                    return()
    
    menu = """
============================ DELETE SECURITY GROUP ============================
    """
    print(menu)
    print(f"Você deseja mesmo deletar o security group {security_groups_list[menu_ans-1]}?")

    ans = input("[s/n]: ")

    if ans == "s":
        with open(".auto.tfvars.json", 'r+') as f:
            data = json.load(f)
            data["security_groups"].pop(menu_ans-1)
            f.seek(0) 
            json.dump(data,f, indent=4)
            f.truncate()
        security_groups_list.pop(menu_ans-1)
    else:
        print("\033[1;31mSecurity group não deletado" + "\033[0m")
        sleep(4)
        return

    print("\033[1;32mSecurity Group sendo deletado em instantes, aguarde..." + "\033[0m")
    sleep(1.5)
    os.system("clear & terraform apply  --auto-approve")
    print("\033[1;32mSecurity Group deletado com sucesso!" + "\033[0m")
    sleep(4)

def show_delete_menu_option_3():
    os.system("clear")
    menu = """
============================ DELETE REGRAS DE INGRESSO ============================
Quais dos security group abaixo você deseja deletar sua regra de ingresso?

    """
    print(menu)

    for i in range(len(security_groups_list)):
        print(f'{i+1}. {security_groups_list[i]}\n')
    print(f"{len(security_groups_list)+1}. Voltar p/ menu principal\n")

    menu_ans = int(input("Digite o número da opção desejada: "))
    while menu_ans not in range(1,len(security_groups_list)+2):
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        menu_ans = int(input("Digite o número da opção desejada: "))
    if menu_ans == len(security_groups_list)+1:
        return
    
    os.system("clear")
    menu = """
============================ DELETE REGRAS DE INGRESSO ============================
Qual das regras abaixo você deseja deletar?
    """

    print(menu)
    with open(".auto.tfvars.json", 'r+') as f:
        data = json.load(f)
        if security_groups_list[menu_ans-1] == "default":
            print("\033[1;31mNão é possível deletar regras do security group default!" + "\033[0m\n")
            input("Pressione qualquer tecla para continuar: ")
            return()
        if len(data["security_groups"][menu_ans-1]["ingress"]) == 1:
            print("\033[1;31mEste security group possui apenas uma regra de ingresso!" + "\033[0m\n")
            input("Pressione qualquer tecla para continuar: ")
            return()
        for i in range(len(data["security_groups"][menu_ans-1]["ingress"])):
            print(f'{i+1}. {data["security_groups"][menu_ans-1]["ingress"][i]}\n')
            print()

        menu_ans_2 = int(input("Digite o número da opção desejada: "))
        while menu_ans_2 not in range(1,len(data["security_groups"][menu_ans-1]["ingress"])+2):
            print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
            print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
            menu_ans_2 = int(input("Digite o número da opção desejada: "))

        os.system("clear")
        menu = """
============================ DELETE REGRAS DE INGRESSO ============================?
    """
        ans = input("Você deseja mesmo deletar a regra de ingresso selecionada? [s/n]: ")
        if ans == "s":
            data["security_groups"][menu_ans-1]["ingress"].pop(menu_ans_2-1)
            f.seek(0)
            json.dump(data,f, indent=4)
            f.truncate()
            print("\033[1;32mRegra de ingresso sendo deletada em instantes, aguarde..." + "\033[0m")
            sleep(1.5)
            os.system("clear & terraform apply  --auto-approve")
            print("\033[1;32mRegra de ingresso deletada com sucesso!" + "\033[0m")
            sleep(4)
            return
        else:
            print("\033[1;31mRegra de ingresso não deletada" + "\033[0m")
            sleep(4)
            return

def show_delete_menu_option_4():
    os.system("clear")
    menu = """
============================ DELETE USUÁRIO ============================
Quais dos usuários abaixo você deseja deletar?

    """
    print(menu)

    for i in range(len(users_list)):
        print(f'{i+1}. {users_list[i]}\n')

    menu_ans = int(input("Digite o número da opção desejada: "))
    while menu_ans not in range(1,len(users_list)+1):
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        menu_ans = int(input("Digite o número da opção desejada: "))

    os.system("clear")
    menu = """
============================ DELETE USUÁRIO ============================
    """
    print(menu)
    print(f"Você deseja mesmo deletar o usuário {users_list[menu_ans-1]}?")

    ans = input("[s/n]: ")

    if ans == "s":
        with open("../users/.auto.tfvars.json", 'r+') as f:
            data = json.load(f)
            data["users"].pop(menu_ans-1)
            f.seek(0) 
            json.dump(data,f, indent=4)
            f.truncate()
        users_list.pop(menu_ans-1)
    else:
        print("\033[1;31mUsuário não deletado" + "\033[0m")
        sleep(4)
        return
    print("\033[1;32mUsuário sendo deletado em instantes, aguarde..." + "\033[0m")
    sleep(1.5)
    os.system("clear & cd .. && cd users && terraform apply  --auto-approve")
    print("\033[1;32mUsuário deletado com sucesso!" + "\033[0m")
    sleep(4)
    return



def show_list_menu():
    os.system("clear")
    menu = """
============================ LISTAR ============================
O que você deseja listar?

1. Instâncias

2. Security Groups

3. Usuários

4. Voltar p/ menu principal
    """
    print(menu)

    menu_ans = int(input("Digite o número da opção desejada: "))
    while menu_ans not in range(1,5):
        print("\033[1;31mOps! Houve algum erro..." + "\033[0m")
        print("Por favor, digite apenas o número dentre as apresentadas. Tente novamente.")
        menu_ans = int(input("Digite o número da opção desejada: "))

    if menu_ans == 1:
        show_list_menu_option_1()
    elif menu_ans == 2:
        show_list_menu_option_2()
    elif menu_ans == 3:
        show_list_menu_option_3()
    else:
        return

def show_list_menu_option_1():
    os.system("clear")
    menu = """
============================ LISTAR INSTÂNCIAS ============================
    """
    print(menu)
    print("As instâncias disponíveis são:\n")
    for i in range(len(instance_list)):
        print(f'{i+1}. {instance_list[i]}\n')
    print("Pressione qualquer tecla para voltar ao menu principal...")
    input()

def show_list_menu_option_2():
    os.system("clear")
    menu = """
============================ LISTAR SECURITY GROUPS ============================
    """
    print(menu)
    print("Os security groups disponíveis são:\n")
    for i in range(len(security_groups_list)):
        print(f'{i+1}. {security_groups_list[i]}\n')
    print("Pressione qualquer tecla para voltar ao menu principal...")
    input()

def show_list_menu_option_3():
    os.system("clear")
    menu = """
============================ LISTAR USUÁRIOS ============================
    """
    print(menu)
    print("Os usuários disponíveis são:\n")
    for i in range(len(users_list)):
        print(f'{i+1}. {users_list[i]}\n')
    print("Pressione qualquer tecla para voltar ao menu principal...")
    input()

def load_var_lists():
    with open("all_vars_lists.json", 'r') as f:
        data = json.load(f)
        instance_list = data["instances"]
        security_groups_list = data["security_groups"]

    with open("../users/users.json", 'r+') as f:
        data = json.load(f)
        users_list = data["users"]
    return instance_list, security_groups_list, users_list

def update_var_lists(instance_list, security_groups_list, users_list):

    with open("all_vars_lists.json", 'w') as f:
        data = {
            "instances": instance_list,
            "security_groups": security_groups_list}
        f.seek(0) 
        json.dump(data,f, indent=4)
        f.truncate()

    with open("../users/users.json", 'w') as f:
        data = {
            "users": users_list}
        f.seek(0) 
        json.dump(data,f, indent=4)
        f.truncate()

################################################### MAIN LOOP ###################################################
while RUNNING:
    instance_list, security_groups_list, users_list = load_var_lists()
    if FIRST_TIME:
        sleep(0.5)
        show_welcome()
        show_menu()
        FIRST_TIME = False
    else:
        show_menu()
    update_var_lists(instance_list, security_groups_list, users_list)
    


