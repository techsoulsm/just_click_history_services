locals {
  api_name = "history_api"
}
module "api_gateway_rest_api" {
  source = "../modules/api_gateway"
  rest_api_name = local.api_name
}

module "get_history" {
  source = "../modules/api_gateway"
  parent_id = lookup(module.api_gateway_rest_api.rest_api_root_id, local.api_name)
  path_part = "get_history"
  rest_api_id = lookup(module.api_gateway_rest_api.rest_api_id, local.api_name)
}

module "get_history_action" {
  source = "../modules/api_gateway"
  path_part = "{get_history_action}"
  parent_id = lookup(module.get_history.rest_api_resource_id, module.get_history.path_part)
  rest_api_id = lookup(module.api_gateway_rest_api.rest_api_id, local.api_name)
  http_method = ["GET"]
  integration_type = "AWS_PROXY"
  function_names = [module.get_history_lambda.lambda_name]
  depends_on = [module.get_history_lambda]
}
#########################################
module "transactions" {
  source = "../modules/api_gateway"
  parent_id = lookup(module.api_gateway_rest_api.rest_api_root_id, local.api_name)
  path_part = "transactions"
  rest_api_id = lookup(module.api_gateway_rest_api.rest_api_id, local.api_name)
}

module "add_transaction" {
  source = "../modules/api_gateway"
  path_part = "{add_transaction_action}"
  parent_id = lookup(module.transactions.rest_api_resource_id, module.transactions.path_part)
  rest_api_id = lookup(module.api_gateway_rest_api.rest_api_id, local.api_name)
  http_method = ["POST"]
  integration_type = "AWS_PROXY"
  function_names = [module.add_transaction_lambda.lambda_name]
  depends_on = [module.add_transaction_lambda]
}
################################
module "deployment" {
  source = "../modules/api_gateway"
  stage_name = var.stage
  rest_api_id = lookup(module.api_gateway_rest_api.rest_api_id, local.api_name)
  depends_on = [module.get_history_action, module.get_history, module.transactions, module.add_transaction]
}
