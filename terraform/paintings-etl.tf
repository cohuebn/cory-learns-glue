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

data "aws_iam_policy_document" "paintings_etl" {
  statement {
    actions = ["s3:HeadObject", "s3:ListObjects", "s3:GetObject"]
    resources = [
      aws_s3_bucket.glue_jobs_source.arn,
      "${aws_s3_bucket.glue_jobs_source.arn}/*",
      aws_s3_bucket.paintings_source.arn,
    "${aws_s3_bucket.paintings_source.arn}/*"]
  }
  statement {
    actions = ["s3:ListBucket", "s3:HeadObject", "s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
    resources = [
      aws_s3_bucket.paintings_processed.arn,
      "${aws_s3_bucket.paintings_processed.arn}/*",
      aws_s3_bucket.glue_temp_files.arn,
      "${aws_s3_bucket.glue_temp_files.arn}/*",
    ]
  }
}

resource "aws_iam_role" "paintings_etl" {
  name                  = "${var.namespace}-paintings-etl"
  assume_role_policy    = data.aws_iam_policy_document.glue_assume_role.json
  force_detach_policies = true
  tags                  = merge(local.tags, { Name = "${var.namespace}-paintings-etl" })
}

resource "aws_iam_role_policy" "paintings_etl" {
  name   = aws_iam_role.paintings_etl.name
  role   = aws_iam_role.paintings_etl.id
  policy = data.aws_iam_policy_document.paintings_etl.json
}

resource "aws_iam_role_policy_attachment" "paintings_etl_glue" {
  role       = aws_iam_role.paintings_etl.id
  policy_arn = local.glue_service_role_arn
}

resource "aws_glue_crawler" "csv_paintings_source" {
  database_name = aws_glue_catalog_database.paintings.name
  name          = "csv-paintings-source"
  role          = aws_iam_role.paintings_etl.arn
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

resource "aws_glue_crawler" "csv_paintings_processed" {
  database_name = aws_glue_catalog_database.paintings.name
  name          = "csv-paintings-processed"
  role          = aws_iam_role.paintings_etl.arn
  tags          = local.tags

  s3_target {
    path = "s3://${aws_s3_bucket.paintings_processed.bucket}"
  }
}

resource "aws_glue_job" "process_csv_paintings" {
  name              = "process-s3-paintings"
  role_arn          = aws_iam_role.paintings_etl.arn
  glue_version      = "2.0"
  number_of_workers = 2
  worker_type       = "G.1X"

  command {
    script_location = "s3://${aws_s3_bucket.glue_jobs_source.bucket}/process_s3_paintings.py"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"   = "python"
    "--extra-py-files" = "s3://${aws_s3_bucket.glue_jobs_source.bucket}/cory.etl-0.0.1-py3-none-any.whl"
    "--TempDir"        = "s3://${aws_s3_bucket.glue_temp_files.bucket}/process_s3_paintings/"
    # Underscores used for custom params per this doc: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-get-resolved-options.html
    "--input_database"   = aws_glue_crawler.csv_paintings_source.database_name
    "--input_table"      = replace(aws_s3_bucket.paintings_source.bucket, "-", "_") # Glue crawler naming convention uses underscores on created tables
    "--processed_bucket" = aws_s3_bucket.paintings_processed.bucket
  }
}

resource "aws_glue_workflow" "process_paintings" {
  name = "${var.namespace}-process-paintings"
}

resource "aws_glue_trigger" "run_paintings_source_crawler" {
  name          = "${var.namespace}-run-source-crawler"
  type          = "ON_DEMAND"
  workflow_name = aws_glue_workflow.process_paintings.name

  actions {
    crawler_name = aws_glue_crawler.csv_paintings_source.name
  }
}

resource "aws_glue_trigger" "run_process_csv_paintings" {
  name          = "${var.namespace}-run-process-csv-job"
  type          = "CONDITIONAL"
  workflow_name = aws_glue_workflow.process_paintings.name

  actions {
    job_name = aws_glue_job.process_csv_paintings.name
  }

  predicate {
    conditions {
      crawler_name = aws_glue_crawler.csv_paintings_source.name
      crawl_state  = "SUCCEEDED"
    }
  }
}

resource "aws_glue_trigger" "run_paintings_processed_crawler" {
  name          = "${var.namespace}-run-processed-crawler"
  type          = "CONDITIONAL"
  workflow_name = aws_glue_workflow.process_paintings.name

  actions {
    crawler_name = aws_glue_crawler.csv_paintings_processed.name
  }

  predicate {
    conditions {
      job_name = aws_glue_job.process_csv_paintings.name
      state    = "SUCCEEDED"
    }
  }
}