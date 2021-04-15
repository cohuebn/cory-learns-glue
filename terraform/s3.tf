resource "aws_s3_bucket" "glue_jobs_source" {
  bucket        = "${var.namespace}-jobs-source"
  tags          = local.tags
  force_destroy = true
}

resource "aws_s3_bucket" "glue_temp_files" {
  bucket        = "${var.namespace}-glue-temp-files"
  tags          = local.tags
  force_destroy = true
}