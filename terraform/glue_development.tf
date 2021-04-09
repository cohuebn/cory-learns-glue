resource "aws_glue_dev_endpoint" "glue_dev" {
  depends_on = [
    aws_security_group_rule.glue_self_egress_all_traffic,
    aws_security_group_rule.glue_self_ingress_all_traffic,
    aws_vpc_endpoint.private_s3
  ]
  name               = "${var.namespace}-development"
  role_arn           = aws_iam_role.glue_dev.arn
  subnet_id          = aws_subnet.vpc_public.id
  security_group_ids = [aws_security_group.glue_dev.id]
}

resource "aws_iam_role" "glue_dev" {
  name               = "${var.namespace}-development"
  assume_role_policy = data.aws_iam_policy_document.glue_dev.json
}

data "aws_iam_policy_document" "glue_dev" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "glue_dev" {
  policy_arn = local.glue_service_role_arn
  role       = aws_iam_role.glue_dev.name
}

resource "aws_security_group" "glue_dev" {
  name   = "${var.namespace}-development"
  tags   = var.tags
  vpc_id = aws_vpc.vpc.id
}

resource "aws_security_group_rule" "glue_self_egress_all_traffic" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = aws_security_group.glue_dev.id
  self              = true
  description       = "Allow all outgoing traffic from within own security group"
}

resource "aws_security_group_rule" "glue_self_ingress_all_traffic" {
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = aws_security_group.glue_dev.id
  self              = true
  description       = "Allow all outgoing traffic from within own security group"
}

resource "aws_security_group_rule" "glue_ssh_ingress_ip_whitelist" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = var.ip_whitelist
  security_group_id = aws_security_group.glue_dev.id
  description       = "Allow incoming SSH traffic from whitelisted addresses"
}

resource "aws_security_group_rule" "glue_ingress_https" {
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = var.ip_whitelist
  security_group_id = aws_security_group.glue_dev.id
  description       = "Allow incoming HTTPS traffic from whitelisted addresses"
}

resource "aws_security_group_rule" "glue_egress_http" {
  type              = "egress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.glue_dev.id
  description       = "Allow outgoing HTTP traffic to anywhere"
}

resource "aws_security_group_rule" "glue_egress_https" {
  type              = "egress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.glue_dev.id
  description       = "Allow outgoing HTTPS traffic to anywhere"
}