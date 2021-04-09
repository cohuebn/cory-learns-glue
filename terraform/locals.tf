locals {
  tags = merge({
    Project   = var.namespace
    Namespace = var.namespace
  }, var.tags)
  glue_service_role_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
  s3_service_name       = "com.amazonaws.${var.region}.s3"
}