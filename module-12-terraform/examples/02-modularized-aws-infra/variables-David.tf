variable "region" { type = string }
variable "name" { type = string default = "module12-demo2" }
variable "key_name" { type = string default = null }
variable "tags" { type = map(string) default = {} }
