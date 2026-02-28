output "control_public_ip" {
  value = aws_instance.control.public_ip
}

output "managed_public_ips" {
  value = [for i in aws_instance.managed : i.public_ip]
}

output "nexus_public_ip" {
  value = aws_instance.nexus.public_ip
}

output "jenkins_public_ip" {
  value = aws_instance.jenkins.public_ip
}
