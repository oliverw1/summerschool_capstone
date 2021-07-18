terraform {
  backend "s3" {
    bucket         = "biostrand-terraform-state-edgzqd"
    region         = "eu-west-1"
    encrypt        = "true"
    key            = "biostrand-1-beta.tfstate"
    dynamodb_table = "biostrand-terraform-statelock"
  }

  required_version = "=0.13.2"
}
