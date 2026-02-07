locals {
  azs = ["${var.region}a", "${var.region}b", "${var.region}c"]
}

module "vpc" {
  source = "../../modules/vpc"
  name           = var.name
  cidr           = "10.30.0.0/16"
  azs            = slice(local.azs, 0, 2)
  public_subnets = ["10.30.1.0/24", "10.30.2.0/24"]
  private_subnets= ["10.30.101.0/24", "10.30.102.0/24"]
  tags = var.tags
}

module "eks" {
  source = "../../modules/eks"
  cluster_name    = var.name
  cluster_version = var.cluster_version
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnets
  tags = var.tags
}
