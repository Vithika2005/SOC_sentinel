resource "aws_s3_bucket" "tfstate" {
  bucket = var.tfstate_bucket_name

  tags = {
    Name = "Terraform State Bucket"
  }
}