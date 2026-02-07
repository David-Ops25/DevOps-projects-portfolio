variable "region" { type = string }
variable "bucket_name" { type = string }
variable "lock_table_name" { type = string default = "terraform-locks" }
variable "tags" { type = map(string) default = {} }
