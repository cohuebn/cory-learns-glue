resource "aws_s3_bucket" "etl_analysis" {
  bucket        = "${var.namespace}-etl-analysis"
  tags          = local.tags
  force_destroy = true
}

resource "aws_athena_workgroup" "etl_analysis" {
  name = "${var.namespace}-analysis"
  tags = local.tags

  configuration {
    result_configuration {
      output_location = "s3://${aws_s3_bucket.etl_analysis.bucket}/athena-results/"
    }
  }
}
