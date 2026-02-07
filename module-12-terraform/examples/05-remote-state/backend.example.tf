terraform {
  backend "s3" {
    bucket         = "REPLACE_ME"
    key            = "module12/terraform.tfstate"
    region         = "REPLACE_ME"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
