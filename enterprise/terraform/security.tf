resource "aws_security_group_rule" "allow_http" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"

  security_group_id = aws_security_group.example_sg.id

  # Intentional vulnerability
  cidr_blocks = ["0.0.0.0/0"]
}