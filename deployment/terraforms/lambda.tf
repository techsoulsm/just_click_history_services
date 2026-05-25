data "archive_file" "archive" {
  output_path = "../../build/artifacts/source.zip"
  type = "zip"
  source_dir = "../../build/package"
}

module "get_history_lambda" {
  source = "../modules/lambdas"
  file_path = "../../build/artifacts/source.zip"
  handler = "app.getHistory"
  lambda_name = "get_history_lambda"
  memory_size = 256
  runtime = "python3.11"
  timeout = 300
  policy_document = [
    data.aws_iam_policy_document.history_service_policy.json
  ]
  depends_on = [
    data.archive_file.archive,
  ]
}

module "add_transaction_lambda" {
  source = "../modules/lambdas"
  file_path = "../../build/artifacts/source.zip"
  handler = "app.add_transaction"
  lambda_name = "add_transaction_lambda"
  memory_size = 256
  runtime = "python3.11"
  timeout = 300
  policy_document = [
    data.aws_iam_policy_document.history_service_policy.json
  ]
  depends_on = [
    data.archive_file.archive,
  ]
}