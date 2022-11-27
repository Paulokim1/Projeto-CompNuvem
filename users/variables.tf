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

