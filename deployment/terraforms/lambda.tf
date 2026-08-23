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
  layers = [
    "arn:aws:lambda:${var.region}:336392948345:layer:AWSSDKPandas-Python311:12"
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
  layers = [
    "arn:aws:lambda:${var.region}:336392948345:layer:AWSSDKPandas-Python311:12"
  ]
}

module "transactions_listener_lambda" {
  source = "../modules/lambdas"
  file_path = "../../build/artifacts/source.zip"
  handler = "transactions_listener.transactions_listener_handler"
  lambda_name = "transactions_listener_lambda"
  memory_size = 256
  runtime = "python3.11"
  timeout = 900
  policy_document = [
    data.aws_iam_policy_document.history_service_policy.json
  ]
  depends_on = [
    data.archive_file.archive,
  ]
  layers = [
    "arn:aws:lambda:${var.region}:336392948345:layer:AWSSDKPandas-Python311:12"
  ]
}

resource "aws_lambda_event_source_mapping" "transactions_listener_mapping" {
  event_source_arn  = module.history_service_table.stream_arn
  function_name     = module.transactions_listener_lambda.lambda_arn
  starting_position = "LATEST"

  filter_criteria {
    filter {
      pattern = jsonencode({
        eventName = ["INSERT", "MODIFY"]
      })
    }
  }
}