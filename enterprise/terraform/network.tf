# Define S3 bucket for storing Terraform state
resource "aws_s3_bucket" "tfstate" {
  bucket = var.tfstate_bucket_name

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "force-delete"
    enabled = true

    expiration {
      days = 365
    }
  }
}

variable "tfstate_bucket_name" {
  type        = string
  description = "The name of the S3 bucket for storing Terraform state."
}
