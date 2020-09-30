terraform {
  backend "s3" {
    bucket  = "requinard-terraform"
    region  = "eu-central-1"
    key     = "luminis/case"
    encrypt = true
  }
}
