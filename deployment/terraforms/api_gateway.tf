locals {
  api_name = "authentication_api"
}
module "api_gateway_rest_api" {
  source = "../modules/api_gateway"
  rest_api_name = local.api_name
}

module "authentication" {
  source = "../modules/api_gateway"
  parent_id = lookup(module.api_gateway_rest_api.rest_api_root_id, local.api_name)
  path_part = "authentication"
  rest_api_id = lookup(module.api_gateway_rest_api.rest_api_id, local.api_name)
}

module "action" {
  source = "../modules/api_gateway"
  path_part = "{action}"
  parent_id = lookup(module.authentication.rest_api_resource_id, module.authentication.path_part)
  rest_api_id = lookup(module.api_gateway_rest_api.rest_api_id, local.api_name)
  http_method = ["POST"]
  integration_type = "AWS_PROXY"
  function_names = [module.authentication_lambda.lambda_name]
  depends_on = [module.authentication_lambda]
}
################################
module "beta_deployment" {
  source = "../modules/api_gateway"
  stage_name = "beta"
  rest_api_id = lookup(module.api_gateway_rest_api.rest_api_id, local.api_name)
  depends_on = [module.action]
}

module "prod_deployment" {
  source = "../modules/api_gateway"
  stage_name = "prod"
  rest_api_id = lookup(module.api_gateway_rest_api.rest_api_id, local.api_name)
  depends_on = [module.action]
}
