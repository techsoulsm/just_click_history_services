data "aws_iam_policy_document" "history_service_policy" {
  statement {
    actions = [
      "dynamodb:*"
    ]
    effect = "Allow"
    resources = [
      "*"
    ]
  }
}

