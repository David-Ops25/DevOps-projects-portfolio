output "public_ip" { value = aws_instance.web.public_ip }
output "ssh_command" {
  value = var.key_name == null ? "No key_name provided" : "ssh -i <path-to-key.pem> ubuntu@${aws_instance.web.public_ip}"
}
