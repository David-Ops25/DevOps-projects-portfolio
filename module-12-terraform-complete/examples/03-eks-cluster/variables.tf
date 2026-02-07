variable "region" { type = string }
variable "name" { type = string default = "module12-eks" }
variable "cluster_version" { type = string default = "1.29" }
variable "tags" { type = map(string) default = {} }
