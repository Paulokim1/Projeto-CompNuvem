# Projeto Terraform-AWS

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

---

Esta aplicação foi desenvolvida com o intuito de provisionar uma instância EC2 na AWS por meio do terminal de uma maneira simples, fácil e amigável. Aqui, você poderá gerenciá-la e adminstrá-la (construir e deletar recursos) de maneira intuitiva. 

A proposta do projeto pode ser encontrada [aqui](https://insper.github.io/computacao-nuvem/projetos/projeto_2022/).

## Como executar o projeto?

1. Definir as variáveis de ambiente locais:

```bash
export AWS_ACCESS_KEY_ID=[seu_access_key]
export AWS_SECRET_ACCESS_KEY=[seu_secret_key]
```

2. Instalar dependências:

- [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

3. Após a instalação das dependências, rode o comando abaixo

```bash
python app.py
```

## O que é possível fazer com o projeto?

- Escolher a região

- Criar:

  - Instâncias
  - Grupo de segurança (com mais de 1 regra)
  - Usuários

- Deletar:

  - Instâncias
  - Grupos de segurança
  - Regras de grupos de segurança
  - Usuários

- Listar:
  - Instâncias
  - Grupos de segurança
  - Usuários

