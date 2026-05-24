# DevOps Project - Mahesh Babu

A Flask web application deployed using a complete DevOps pipeline.

## Tech Stack
- **Application**: Python Flask
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Docker Desktop)
- **Infrastructure**: Terraform + AWS EC2
- **CI/CD**: Jenkins Pipeline
- **Configuration Management**: Ansible

## Architecture
GitHub Push → Jenkins Pipeline → Docker Build → Test → Kubernetes Deploy

## Infrastructure
- EC2 Instance provisioned via Terraform
- Public IP: 44.200.251.44

## Pipeline Stages
1. Clone - pulls code from GitHub
2. Build - builds Docker image
3. Test - runs application tests
4. Deploy - deploys to Kubernetes cluster

## How to Run Locally
```bash
# Run with Docker
docker build -t devops-project .
docker run -p 5000:5000 devops-project

# Run with Kubernetes
kubectl apply -f k8s-deployment.yaml
kubectl port-forward service/devops-project-service 8081:80
```

## Ansible
Ansible playbook available for automated deployment to remote servers.
