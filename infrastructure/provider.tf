provider "aws" {
  region = "eu-west-1"

  // List of allowed, white listed, AWS account IDs to prevent you from mistakenly
  // using an incorrect one (and potentially end up destroying a live environment)
  allowed_account_ids = ["130966031144"]
}