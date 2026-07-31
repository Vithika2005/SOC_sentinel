provider "aws" {
  region = var.region
}

# Vulnerability: Open Ingress Rule (IaC / Checkov target)
resource "aws_security_group" "legacy_sg" {
  name        = "legacy-vulnerable-sg"
  description = "Security group with unrestricted inbound access"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}