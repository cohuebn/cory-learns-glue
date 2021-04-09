resource "aws_s3_bucket" "paintings_source" {
  bucket = "${var.namespace}-paintings-source"
  tags   = local.tags
}

locals {
  bob_ross_paintings_directory = "${path.module}/../datasets/bob-ross-paintings"
}

resource "aws_s3_bucket_object" "bob_ross_painting" {
  for_each = fileset(local.bob_ross_paintings_directory, "*")
  bucket   = aws_s3_bucket.paintings_source.bucket
  key      = "bob-ross/${each.value}"
  source   = "${local.bob_ross_paintings_directory}/${each.value}"
  etag     = filemd5("${local.bob_ross_paintings_directory}/${each.value}")
}