variable "region" { type = string }
variable "project_name" { type = string default = "module12-demo1" }
variable "vpc_cidr" { type = string default = "10.10.0.0/16" }
variable "public_subnet_cidr" { type = string default = "10.10.1.0/24" }
variable "allowed_ssh_cidr" { type = list(string) default = ["0.0.0.0/0"] }
variable "key_name" { type = string default = null }
variable "instance_type" { type = string default = "t3.micro" }
variable "tags" { type = map(string) default = {} }
