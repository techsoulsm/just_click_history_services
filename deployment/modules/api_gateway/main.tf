locals {
  async_header = {"integration.request.header.X-Amz-Invocation-Type": "'Event'"}
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_lambda_function" "lambda" {
  count = length(var.function_names)
  function_name = var.function_names[count.index]
}

resource "aws_api_gateway_rest_api" "rest_api" {
  count = var.rest_api_name == null ? 0 : 1
  name = var.rest_api_name
  endpoint_configuration {
    types = [var.endpoint_type]
  }
  binary_media_types = var.binary_media_types
}

resource "aws_api_gateway_resource" "resource" {
  count = var.path_part == null ? 0 : 1
  parent_id = var.parent_id
  path_part = var.path_part
  rest_api_id = var.rest_api_id
}

resource "aws_api_gateway_method" "method" {
  count = length(var.http_method)
  authorization = var.authorization_type
  authorizer_id = var.authorizer_id
  http_method = var.http_method[count.index]
  resource_id = aws_api_gateway_resource.resource.*.id[0]
  rest_api_id = var.rest_api_id
  request_parameters = {for k,v in var.request_parameters: "method.request.${k}" => v}
}

resource "aws_api_gateway_integration" "integration" {
  count = length(var.http_method)
  http_method = aws_api_gateway_method.method.*.http_method[count.index]
  resource_id = aws_api_gateway_resource.resource.*.id[0]
  rest_api_id = var.rest_api_id
  type        = var.integration_type
  uri         = data.aws_lambda_function.lambda.*.invoke_arn[count.index]
  cache_key_parameters = [for i in var.cache_key_parameters: "method.request.path.${i}"]
  cache_namespace      = var.cache_namespace
  timeout_milliseconds = var.timeout
  integration_http_method = "POST"
  request_templates = var.request_templates
  request_parameters = var.async_invoke ? local.async_header : {}
  passthrough_behavior = var.passthrough_behavior
  content_handling     = var.content_handling
  depends_on = [aws_api_gateway_method.method]
}

resource "aws_api_gateway_method" "options_method" {
  count = length(var.http_method) > 0 ? 1: 0
  http_method = "OPTIONS"
  resource_id = aws_api_gateway_resource.resource.*.id[0]
  rest_api_id = var.rest_api_id
  authorization = "None"
  depends_on = [aws_api_gateway_method.method]
}

resource "aws_api_gateway_method_response" "options_response" {
  count = length(var.http_method) > 0 ? 1: 0
  http_method = aws_api_gateway_method.options_method.*.http_method[0]
  resource_id = aws_api_gateway_resource.resource.*.id[0]
  rest_api_id = var.rest_api_id
  status_code = 200
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin" = true
  }
  response_models = {
    "application/json" = "Empty"
  }
  depends_on = [aws_api_gateway_method.options_method]
}

resource "aws_api_gateway_integration" "options_integration" {
  count = length(var.http_method) > 0 ? 1: 0
  http_method = aws_api_gateway_method.options_method.*.http_method[0]
  resource_id = aws_api_gateway_resource.resource.*.id[0]
  rest_api_id = var.rest_api_id
  type = "MOCK"
  request_templates = {
    "application/json" = <<EOF
{"statusCode": 200}
EOF
  }
  depends_on = [aws_api_gateway_method.options_method]
}

resource "aws_api_gateway_integration_response" "options_integration_response" {
  count = length(var.http_method) > 0 ? 1: 0
  http_method = aws_api_gateway_method.options_method.*.http_method[0]
  resource_id = aws_api_gateway_resource.resource.*.id[0]
  rest_api_id = var.rest_api_id
  status_code = 200
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'*'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }
  depends_on = [aws_api_gateway_integration.options_integration]
}

resource "aws_api_gateway_method_response" "method_response" {
  count = length(var.http_method)
  http_method = aws_api_gateway_method.method.*.http_method[count.index]
  resource_id = aws_api_gateway_resource.resource.*.id[0]
  rest_api_id = var.rest_api_id
  status_code = 200
  response_parameters = {
//    "method.response.header.Access-Control-Allow-Headers" = true,
//    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin" = true
  }
  response_models = {
    "application/json" = "Empty"
  }
  depends_on = [aws_api_gateway_method.method]
}

resource "aws_api_gateway_integration_response" "integration_response" {
  count = length(var.http_method)
  http_method = aws_api_gateway_method.method.*.http_method[count.index]
  resource_id = aws_api_gateway_resource.resource.*.id[0]
  rest_api_id = var.rest_api_id
  status_code = 200
  response_parameters = {
//    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
//    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }
  depends_on = [aws_api_gateway_integration.integration]
}


resource "aws_lambda_permission" "lambda_permission" {
  count             = length(var.function_names)
  action            = "lambda:InvokeFunction"
  principal         = "apigateway.amazonaws.com"
  function_name     = var.function_names[count.index]
  source_arn = "arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.method.*.http_method[count.index]}${aws_api_gateway_resource.resource.*.path[0]}"
}

resource "aws_api_gateway_deployment" "deployment" {
  count      = var.stage_name == null ? 0 : 1
  rest_api_id = var.rest_api_id

  triggers = {
    # Redeploy when any of these resources change
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.resource,
      aws_api_gateway_method.method,
      aws_api_gateway_integration.integration,
    ]))
  }

  depends_on = [aws_api_gateway_integration.integration]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  count         = var.stage_name == null ? 0 : 1
  deployment_id = aws_api_gateway_deployment.deployment[0].id
  rest_api_id   = var.rest_api_id
  stage_name    = var.stage_name
}

resource "aws_api_gateway_gateway_response" "response_4xx" {
  count = var.rest_api_name == null ? 0 : 1
  rest_api_id   = aws_api_gateway_rest_api.rest_api.*.id[0]
  status_code   = "401"
  response_type = "DEFAULT_4XX"

  response_templates = {
    "application/json" = "{\"message\":$context.error.messageString}"
  }

  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin" = "'*'",
    "gatewayresponse.header.Access-Control-Allow-Headers" = "'*'",
    "gatewayresponse.header.Access-Control-Allow-Methods" = "'OPTIONS,POST,GET'"
  }
  depends_on = [aws_api_gateway_rest_api.rest_api]
}

resource "aws_api_gateway_gateway_response" "response_5xx" {
  count = var.rest_api_name == null ? 0 : 1
  rest_api_id   = aws_api_gateway_rest_api.rest_api.*.id[0]
  status_code   = "503"
  response_type = "DEFAULT_5XX"

  response_templates = {
    "application/json" = "{\"message\":$context.error.messageString}"
  }

  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin" = "'*'",
    "gatewayresponse.header.Access-Control-Allow-Headers" = "'*'",
    "gatewayresponse.header.Access-Control-Allow-Methods" = "'OPTIONS,POST,GET'"
  }
  depends_on = [aws_api_gateway_rest_api.rest_api]
}