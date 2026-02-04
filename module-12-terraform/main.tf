terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = ">= 4.0"
    }
    http = {
      source  = "hashicorp/http"
      version = ">= 3.0"
    }
    local = {
      source  = "hashicorp/local"
      version = ">= 2.0"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

provider "aws" {
  region = var.aws_region
}

variable "key_name" {
  type    = string
  default = "tf-ec2-key"
}

resource "tls_private_key" "ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "private_key_pem" {
  filename        = "${path.module}/${var.key_name}.pem"
  content         = tls_private_key.ssh.private_key_pem
  file_permission = "0400"
}

resource "aws_key_pair" "this" {
  key_name   = var.key_name
  public_key = tls_private_key.ssh.public_key_openssh
}

data "http" "myip" {
  url = "https://api.ipify.org"
}

locals {
  my_ip_cidr = "${chomp(data.http.myip.response_body)}/32"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

output "aws_region" {
  value = var.aws_region
}

output "key_name" {
  value = aws_key_pair.this.key_name
}

output "my_ip" {
  value = local.my_ip_cidr
}

output "instance_type" {
  value = var.instance_type
}

module "ec2" {
  source = "./modules/ec2"

  aws_region    = var.aws_region
  key_name      = aws_key_pair.this.key_name
  my_ip_cidr    = local.my_ip_cidr
  instance_type = var.instance_type
}

output "ec2_public_ip" {
  value = module.ec2.public_ip
}

output "ssh_command" {
  value = "ssh -i ${path.module}/${var.key_name}.pem ec2-user@${module.ec2.public_ip}"
}
