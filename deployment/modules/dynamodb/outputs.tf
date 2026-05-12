output "dynamodb_arn" {
  value = try(tolist(aws_dynamodb_table.table.*.arn)[0], "")
}

output "stream_arn" {
  value = try(tolist(aws_dynamodb_table.table.*.stream_arn)[0], "")
}
