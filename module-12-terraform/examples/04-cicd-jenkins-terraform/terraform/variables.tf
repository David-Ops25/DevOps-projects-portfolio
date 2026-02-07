variable "region" { type = string }
variable "name" { type = string default = "module12-cicd" }
variable "key_name" { type = string }
variable "tags" { type = map(string) default = {} }
