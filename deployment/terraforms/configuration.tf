# # API details
# resource "null_resource" "authorizer_lambda_details" {
#         triggers = {
#     always_run = timestamp()
#   }

#   provisioner "local-exec" {
#     command = <<EOF
# aws dynamodb put-item --table-name configurationDNS --profile ${var.profile} --region ${var.region} --item '{"configurationName": {"S": "All"},"configurationGroup": {"S": "${var.stage}_authorizer_lambda_details"},"resource_type": {"S": "lambda"},"lambda_arn": {"S": "${module.authorizer_lambda.lambda_arn}"}}'
# EOF
# }
# }
