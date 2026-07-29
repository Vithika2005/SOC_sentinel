variable "region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-west-2"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for the subnet."
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "Availability zone for the subnet."
  type        = string
  default     = "us-west-2a"
}

variable "tfstate_bucket_name" {
  description = "Name of the S3 bucket to store Terraform state."
  type        = string
  default     = "your-tfstate-bucket-name"
}

variable "peer_vpc_id" {
  description = "ID of the VPC to peer with."
  type        = string
  default     = "vpc-1234567890abcdef0"
}
