resource "aws_s3_bucket" "bucket" {
  bucket = var.name
}

resource "aws_s3_bucket_versioning" "bucket_versioning" {
  bucket = aws_s3_bucket.bucket.id
  versioning_configuration {
    status = var.versioning_status
  }
  depends_on = [aws_s3_bucket.bucket]
}

resource "aws_s3_bucket_lifecycle_configuration" "lifecycle" {
  count = var.archive ? 1: 0
  bucket = aws_s3_bucket.bucket.id
  rule {
    id     = "archive"
    status = "Enabled"
    transition {
      days = 30
      storage_class = "GLACIER"
    }

  }
}