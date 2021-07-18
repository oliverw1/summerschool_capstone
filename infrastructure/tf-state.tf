terraform {
  backend "s3" {
    bucket         = "dm-summer-capstone"
    region         = "eu-west-1"
    encrypt        = "true"
    key            = "summer-capstone.tfstate"
    dynamodb_table = "summer-capstone-statelock"
  }
}
