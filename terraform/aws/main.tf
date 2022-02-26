provider "aws" {
  region = "eu-west-1"
}


# module "vpc" {
#   source = "terraform-aws-modules/vpc/aws"

#   name = "my-vpc"
#   cidr = "10.0.0.0/16"

#   azs             = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
#   private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
#   public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

#   enable_nat_gateway = true
#   enable_vpn_gateway = true
#   single_nat_gateway = true

#   enable_dns_hostnames = true
#   enable_dns_support   = true

#   tags = {
#     Terraform   = "true"
#     Environment = "dev"
#   }
# }


data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  partition  = data.aws_partition.current.partition
}

variable "region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "eu-west-1"
}

data "aws_vpc" "my_vpc" {
  id = var.vpcid
}

data "aws_subnets" "example" {
  filter {
    name   = "vpc-id"
    values = var.subnets
  }
}
