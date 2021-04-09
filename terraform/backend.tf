terraform {
  backend "remote" {
    workspaces {
      name = "glue-learning"
    }
  }
}
