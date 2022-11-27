terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "vpc_east-1" {
    cidr_block = "10.0.0.0/24"
    enable_dns_hostnames = true
    instance_tenancy     = "default"

    tags = {
        Name = "vpc_east-1"
    }
} 

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.vpc_east-1.id

  tags = {
    Name = "Public RT"
  }
}

resource "aws_subnet" "subnet_east-1" {
    vpc_id = aws_vpc.vpc_east-1.id
    availability_zone = "us-east-1a"
    map_public_ip_on_launch = true
    cidr_block = "10.0.0.0/24"

    tags = {
        Name = "subnet_east-1"
    }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.subnet_east-1.id
  route_table_id = aws_route_table.public_rt.id
}

########### USER ###########
resource "aws_iam_user" "user" {
  for_each = { for user in var.users : user.name => user }
  name     = each.value.name
  path = "/"
}

########### USER POLICY ###########
# create the inline policy
data "aws_iam_policy_document" "policy_doc" {
  for_each = { for user in var.users : user.name => user }
  dynamic "statement" {
    for_each = each.value.restrictions
    content {
        actions   = each.value["restrictions"].actions
        resources = each.value["restrictions"].resources
    }
  }
}

# create the policy
resource "aws_iam_policy" "policy" {
  for_each = { for user in var.users : user.name => user }
  policy      = data.aws_iam_policy_document.policy_doc[each.value.name].json
}


# attach policy to user
resource "aws_iam_user_policy_attachment" "user_policy_attachment" {
  for_each = { for user in var.users : user.name => user }
  user      = aws_iam_user.user[each.value.name].name
  policy_arn = aws_iam_policy.policy[each.value.name].arn
}

########### SECURITY GROUP ###########
resource "aws_security_group" "app_server" {
    for_each = { for sg in var.security_groups : sg.name => sg } 

    name        = each.value.name
    description = "Allow inbound traffic"
    vpc_id      = aws_vpc.vpc_east-1.id

    dynamic "ingress" {
        for_each = each.value.ingress
        content {
            from_port   = ingress.value.from_port
            to_port     = ingress.value.to_port
            protocol    = ingress.value.protocol
            cidr_blocks = [ingress.value.cidr_blocks[0]]
            }
        }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}



resource "aws_instance" "app_server" {
    for_each = { for instance in var.instances : instance.name => instance }

    ami           = each.value.ami
    instance_type = each.value.instance_type
    key_name = "paulo-key"
    vpc_security_group_ids = [aws_security_group.app_server[each.value.sg-name].id]
    subnet_id     = aws_subnet.subnet_east-1.id
    tags = {
        Name = each.value.name
    }
}