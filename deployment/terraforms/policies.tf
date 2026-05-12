data "aws_iam_policy_document" "cognito_policy" {
  statement {
    actions = [
      "cognito:*",
      "cognito-idp:*",
      "dynamodb:*"
    ]
    effect = "Allow"
    resources = [
      "*"
    ]
  }
}

