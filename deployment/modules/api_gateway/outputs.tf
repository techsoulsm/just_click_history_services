output "rest_api_id" {
  value = zipmap(aws_api_gateway_rest_api.rest_api.*.name, aws_api_gateway_rest_api.rest_api.*.id)
}

output "rest_api_root_id" {
  value = zipmap(aws_api_gateway_rest_api.rest_api.*.name, aws_api_gateway_rest_api.rest_api.*.root_resource_id)
}

output "rest_api_resource_id" {
  value = zipmap(aws_api_gateway_resource.resource.*.path_part, aws_api_gateway_resource.resource.*.id)
}

output "path_part" {
  value = var.path_part
}

output "rest_api_resource_path" {
  value = var.path_part == null ? "" : tolist(aws_api_gateway_resource.resource.*.path)[0]
}

output "stage_name" {
  value = var.stage_name
}