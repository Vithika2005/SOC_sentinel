provider "aws" {
  region = var.region
}

# Define VPC
resource "aws_vpc" "example_vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "ExampleVPC"
  }
}

# Define Security Group
resource "aws_security_group" "example_sg" {
  name        = "example-sg"
  description = "Allow traffic from all IPs"
  vpc_id      = aws_vpc.example_vpc.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"

    # Intentional vulnerability for Checkov
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"

    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Define Subnet
resource "aws_subnet" "example_subnet" {
  vpc_id            = aws_vpc.example_vpc.id
  cidr_block        = var.subnet_cidr
  availability_zone = var.availability_zone
}