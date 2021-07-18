locals {
  tags = merge(
    {
      "Environment" = var.environment,
      "Terraform"   = "True"
    },
  var.tags)
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.70.0"

  name = "vpc-${var.environment}"
  cidr = var.vpc_cidr

  azs = var.azs

  private_subnets = var.private_subnet_cidrs
  private_subnet_tags = {
    Type = "private"
  }
  public_subnets = var.public_subnet_cidrs
  public_subnet_tags = {
    Type = "public"
  }
  enable_dns_hostnames = true
  enable_dns_support   = true

  single_nat_gateway     = true
  enable_nat_gateway     = true
  one_nat_gateway_per_az = false

  enable_s3_endpoint       = true


  tags = local.tags
}