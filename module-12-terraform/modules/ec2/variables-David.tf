variable "name" { type = string }
variable "ami_id" { type = string }
variable "instance_type" { type = string }
variable "subnet_id" { type = string }
variable "vpc_id" { type = string }
variable "allowed_ssh_cidr" { type = list(string) default = ["0.0.0.0/0"] }
variable "allowed_http_cidr" { type = list(string) default = ["0.0.0.0/0"] }
variable "key_name" { type = string default = null }
variable "user_data" { type = string default = null }
variable "tags" { type = map(string) default = {} }
