resource "aws_glue_catalog_database" "paintings" {
  name = "${var.namespace}-paintings"
}

data "aws_iam_policy_document" "glue_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "csv_paintings_crawler" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.paintings_source.arn}/*"]
  }
}

resource "aws_iam_role" "csv_paintings_crawler" {
  name                  = "${var.namespace}-csv-paintings-crawler"
  assume_role_policy    = data.aws_iam_policy_document.glue_assume_role.json
  force_detach_policies = true
  tags                  = merge(local.tags, { Name = "${var.namespace}-csv-paintings-crawler" })
}

resource "aws_iam_role_policy" "csv_paintings_crawler" {
  name   = aws_iam_role.csv_paintings_crawler.name
  role   = aws_iam_role.csv_paintings_crawler.id
  policy = data.aws_iam_policy_document.csv_paintings_crawler.json
}

resource "aws_iam_role_policy_attachment" "csv_paintings_crawler_glue" {
  role       = aws_iam_role.csv_paintings_crawler.id
  policy_arn = local.glue_service_role_arn
}

resource "aws_glue_crawler" "csv_paintings" {
  database_name = aws_glue_catalog_database.paintings.name
  name          = "csv-paintings"
  role          = aws_iam_role.csv_paintings_crawler.arn
  tags          = local.tags

  s3_target {
    path = "s3://${aws_s3_bucket.paintings_source.bucket}"
  }
}

resource "aws_s3_bucket" "paintings_processed" {
  bucket        = "${var.namespace}-paintings-processed"
  tags          = local.tags
  force_destroy = true
}

data "aws_iam_policy_document" "process_csv_paintings" {
  statement {
    actions   = ["s3:HeadObject", "s3:ListObjects", "s3:GetObject"]
    resources = [aws_s3_bucket.glue_jobs_source.arn, "${aws_s3_bucket.glue_jobs_source.arn}/*"]
  }
  statement {
    actions   = ["s3:HeadObject", "s3:GetObject"]
    resources = ["${aws_s3_bucket.paintings_source.arn}/*"]
  }
  statement {
    actions = ["s3:ListBucket", "s3:PutObject", "s3:DeleteObject"]
    resources = [
      aws_s3_bucket.paintings_processed.arn,
      "${aws_s3_bucket.paintings_processed.arn}/*",
      aws_s3_bucket.glue_temp_files.arn,
      "${aws_s3_bucket.glue_temp_files.arn}/*",
    ]
  }
}

resource "aws_iam_role" "process_csv_paintings" {
  name                  = "${var.namespace}-process-csv-paintings"
  assume_role_policy    = data.aws_iam_policy_document.glue_assume_role.json
  force_detach_policies = true
  tags                  = merge(local.tags, { Name = "${var.namespace}-process-csv-paintings" })
}

resource "aws_iam_role_policy" "process_csv_paintings" {
  name   = aws_iam_role.process_csv_paintings.name
  role   = aws_iam_role.process_csv_paintings.id
  policy = data.aws_iam_policy_document.process_csv_paintings.json
}

resource "aws_iam_role_policy_attachment" "process_csv_paintings_glue" {
  role       = aws_iam_role.process_csv_paintings.id
  policy_arn = local.glue_service_role_arn
}

resource "aws_glue_job" "process_csv_paintings" {
  name              = "process-s3-paintings"
  role_arn          = aws_iam_role.process_csv_paintings.arn
  glue_version      = "2.0"
  number_of_workers = 10
  worker_type       = "G.1X"

  command {
    script_location = "s3://${aws_s3_bucket.glue_jobs_source.bucket}/process-s3-paintings.py"
  }

  default_arguments = {
    "--job-language"   = "python"
    "--extra-py-files" = "s3://${aws_s3_bucket.glue_jobs_source.bucket}/cory.etl-0.0.1-py3-none-any.whl"
    "--TempDir"        = "s3://${aws_s3_bucket.glue_temp_files.bucket}/process-s3-paintings/"
    # Underscores used for custom params per this doc: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-get-resolved-options.html
    "--input_database"   = aws_glue_crawler.csv_paintings.database_name
    "--input_table"      = aws_s3_bucket.paintings_source.bucket
    "--processed_bucket" = aws_s3_bucket.paintings_processed.bucket
  }
}