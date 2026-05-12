data "archive_file" "archive" {
  output_path = "../../build/artifacts/source.zip"
  type = "zip"
  source_dir = "../../build/package"
}

module "history_service_lambda" {
  source = "../modules/lambdas"
  file_path = "../../build/artifacts/source.zip"
  handler = "app.lambdaHandler"
  lambda_name = "history_service_lambda"
  memory_size = 256
  runtime = "python3.11"
  timeout = 300
  policy_document = [
    data.aws_iam_policy_document.cognito_policy.json
  ]
  depends_on = [
    data.archive_file.archive,
  ]
}