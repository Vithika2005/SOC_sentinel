variable "aws_region" {
  type        = string
  description = "AWS region for deployment"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Environment name (e.g., dev, staging, prod)"
  default     = "dev"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "tfstate_bucket_name" {
  type        = string
  description = "Unique name for the Terraform state S3 bucket"
  default     = "enterprise-tfstate-bucket-local"
}