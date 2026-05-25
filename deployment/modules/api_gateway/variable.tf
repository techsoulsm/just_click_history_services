variable "rest_api_name" {
  default = null
  description = "Name of the Rest API"
}

variable "async_invoke" {
  default = false
}

variable "request_templates" {
  default = null
}

variable "endpoint_type" {
  default = "EDGE"
}

variable "parent_id" {
  default = null
  description = "Parent Id of the api gateway resource if no resource apigateway as root resource "
}

variable "path_part" {
  default = null
  description = "path  of the resource to be created"
}

variable "rest_api_id" {
  default = null
  description = "id of the Rest api top attach to resource"
}

variable "http_method" {
  default = []
  description = "HTTP method for api resource"
}

variable "integration_type" {
  default = "AWS_PROXY"
  description = "AWS Method Integration type e.g.:`MOCK`, `AWS_PROXY`, etc "
}

//variable "lambda_invoke_arn" {
//  default = null
//  description = "used to invoke lambda from api gateway"
//}

variable "cache_key_parameters" {
  default = []
  description = "cache key parameters"
}

variable "cache_namespace" {
  default = null
  description = "Name of the cache"
}

variable "binary_media_types" {
  type = list(string)
  default = []
  description = "List of binary media types that API Gateway will treat as binary (e.g. multipart/form-data, application/octet-stream)"
}

variable "passthrough_behavior" {
  type = string
  default = "WHEN_NO_MATCH"
  description = "Integration passthrough behavior for API Gateway integrations"
}

variable "content_handling" {
  type = string
  default = null
  description = "Optional content handling for integration (CONVERT_TO_TEXT or CONVERT_TO_BINARY). Leave null to omit."
}

variable "timeout" {
  default = null
  description = "Timeout seconds from api gateway"
}

variable "request_parameters" {
  default = {}
  description = "request parameters eg. pathParameters, queryStringParameters, headers"
}

variable "function_names" {
  default = []
  description = "AWS Lambda function name"
}

variable "stage_name" {
  default = null
  description = "AWS api gateway stage name"
}

variable "authorization_type" {
  default = "None"
}

variable "authorizer_id" {
  default = null
}