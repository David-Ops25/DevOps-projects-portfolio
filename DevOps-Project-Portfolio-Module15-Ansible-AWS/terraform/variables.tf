variable "aws_region" {
  type        = string
  description = "AWS region"
}

variable "project_name" {
  type        = string
  description = "Project tag prefix/name"
}

variable "key_name" {
  type        = string
  description = "Existing EC2 Key Pair name"
}

variable "my_ip_cidr" {
  type        = string
  description = "Your public IP in CIDR form, e.g. 82.20.156.133/32"
}

variable "managed_count" {
  type        = number
  description = "Number of managed nodes"
  default     = 2
}
