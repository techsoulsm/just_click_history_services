data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

#data "aws_iam_account_alias" "current" {}

terraform {
  backend "s3" {}
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = var.region
  profile = var.profile
}

provider "aws" {
  alias = "west"
  region = "eu-west-1"
}
