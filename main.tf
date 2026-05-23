provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "devops_ec2" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"

  tags = {
    Name = "devops-project-mahesh"
  }
}

output "public_ip" {
  value = aws_instance.devops_ec2.public_ip
}