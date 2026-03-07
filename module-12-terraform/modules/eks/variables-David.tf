variable "cluster_name" { type = string }
variable "cluster_version" { type = string default = "1.29" }
variable "vpc_id" { type = string }
variable "subnet_ids" { type = list(string) }
variable "tags" { type = map(string) default = {} }

variable "node_group_instance_types" { type = list(string) default = ["t3.medium"] }
variable "node_group_desired_size" { type = number default = 2 }
variable "node_group_min_size" { type = number default = 1 }
variable "node_group_max_size" { type = number default = 3 }
