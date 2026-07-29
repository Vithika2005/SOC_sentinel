provider "aws" {
  region = var.region
}

# Define security group
resource "aws_security_group" "example_sg" {
  name        = "example-sg"
  description = "Allow traffic from all IPs"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Define subnet
resource "aws_subnet" "example_subnet" {
  vpc_id            = var.vpc_id
  cidr_block        = var.subnet_cidr
  availability_zone = var.availability_zone
}

# Define VPC
resource "aws_vpc" "example_vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "ExampleVPC"
  }
}

variable "region" {
  type        = string
  description = "The AWS region to deploy resources in."
}

variable "vpc_id" {
  type        = string
  description = "The VPC ID where the subnet is located."
}

variable "subnet_cidr" {
  type        = string
  description = "The CIDR block for the subnet."
}

variable "availability_zone" {
  type        = string
  description = "The availability zone for the subnet."
}
