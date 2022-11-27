# Path: main.tf

variable "users" {
    type = list(object({
        name = string
        restrictions = object({
            actions = list(string)
            resources = list(string)
        })
    }))
}

variable "security_groups" {
    type = list(object({
        name = string
        ingress = list(object({
            from_port = number
            to_port = number
            protocol = string
            cidr_blocks = list(string)
        }))
    }))
}

variable "instances" {
    type = list(object({
        name = string
        ami = string
        instance_type = string
        sg-name = string
    }))
}

