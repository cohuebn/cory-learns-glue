provider "aws" {
  region = var.region
}

terraform {
  required_providers {
    aws = {
      source  = "aws"
      version = "3.35.0"
    }
  }
}
