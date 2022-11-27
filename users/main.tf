terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">= 1.2.0"
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