resource "aws_glue_catalog_database" "paintings" {
  name = "${var.namespace}-paintings"
}

data "aws_iam_policy_document" "csv_paintings" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.paintings_source.arn}/*"]
  }
}

data "aws_iam_policy_document" "csv_paintings_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "csv_paintings" {
  name                  = "${var.namespace}-csv-paintings"
  assume_role_policy    = data.aws_iam_policy_document.csv_paintings_assume_role.json
  force_detach_policies = true
  tags                  = merge(local.tags, { Name = "${var.namespace}-csv-paintings" })
}

resource "aws_iam_role_policy" "csv_paintings" {
  name   = aws_iam_role.csv_paintings.name
  role   = aws_iam_role.csv_paintings.id
  policy = data.aws_iam_policy_document.csv_paintings.json
}

resource "aws_iam_role_policy_attachment" "csv_paintings_glue" {
  role       = aws_iam_role.csv_paintings.id
  policy_arn = local.glue_service_role_arn
}

resource "aws_glue_crawler" "csv_paintings" {
  database_name = aws_glue_catalog_database.paintings.name
  name          = "csv-paintings"
  role          = aws_iam_role.csv_paintings.arn
  tags          = local.tags

  s3_target {
    path = "s3://${aws_s3_bucket.paintings_source.bucket}"
  }
}