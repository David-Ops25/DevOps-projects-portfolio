output "backend_example" {
  value = <<EOT
terraform {
  backend "s3" {
    bucket         = "${aws_s3_bucket.tf_state.bucket}"
    key            = "module12/terraform.tfstate"
    region         = "${var.region}"
    dynamodb_table = "${aws_dynamodb_table.lock.name}"
    encrypt        = true
  }
}
EOT
}
