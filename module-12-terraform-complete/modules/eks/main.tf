module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  eks_managed_node_groups = {
    default = {
      instance_types = var.node_group_instance_types
      desired_size   = var.node_group_desired_size
      min_size       = var.node_group_min_size
      max_size       = var.node_group_max_size
    }
  }

  tags = var.tags
}
