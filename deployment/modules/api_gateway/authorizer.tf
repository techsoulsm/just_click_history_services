data "aws_cognito_user_pools" "selected" {
  count = var.pool_name == null ? 0 : 1
  name = var.pool_name
}

resource "aws_api_gateway_authorizer" "authorizer" {
  count = var.pool_name == null ? 0 : 1
  name = var.authorizer_name
  rest_api_id = var.rest_api_id
  identity_source = "method.request.header.${var.auth_header_parm}"
  type = var.authorizer_type
  provider_arns = data.aws_cognito_user_pools.selected.*.arns[0]
}

variable "authorizer_name" {
  default = "authorizer"
}

variable "authorizer_type" {
  default = "COGNITO_USER_POOLS"
}

variable "auth_header_parm" {
  default = "Authorization"
}

variable "pool_name" {
  default = null
}

output "authorization_id" {
  value = var.pool_name == null ? null : element(tolist(aws_api_gateway_authorizer.authorizer.*.id), 0)
}

