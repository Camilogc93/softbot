# main.tf

provider "aws" {
  region = var.region
}

# Create ECR Repository
resource "aws_ecr_repository" "app_repo" {
  name                 = var.app_name
  image_tag_mutability = "MUTABLE"

  tags = {
    Name = "${var.app_name}-ecr-repo"
  }
}

# IAM Role for App Runner Service
resource "aws_iam_role" "apprunner_role" {
  name = "${var.app_name}-apprunner-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "build.apprunner.amazonaws.com"
      }
    }]
  })

  tags = {
    Name = "${var.app_name}-apprunner-role"
  }
}

# IAM Policy for App Runner to Access ECR
resource "aws_iam_policy" "apprunner_ecr_policy" {
  name        = "${var.app_name}-apprunner-ecr-policy"
  description = "Policy to allow App Runner to access ECR"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ],
        Resource = aws_ecr_repository.app_repo.arn
      },
      {
        Effect   = "Allow",
        Action   = [
          "ecr:GetAuthorizationToken"
        ],
        Resource = "*"
      }
    ]
  })

  tags = {
    Name = "${var.app_name}-apprunner-ecr-policy"
  }
}

# Attach Policy to IAM Role
resource "aws_iam_role_policy_attachment" "apprunner_ecr_attachment" {
  role       = aws_iam_role.apprunner_role.name
  policy_arn = aws_iam_policy.apprunner_ecr_policy.arn
}

# Build and Push Docker Image to ECR
resource "null_resource" "docker_build_push" {
  provisioner "local-exec" {
    command = <<EOF
      aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${aws_ecr_repository.app_repo.repository_url}
      docker build -t ${var.app_name} ${var.app_dir}
      docker tag ${var.app_name}:latest ${aws_ecr_repository.app_repo.repository_url}:latest
      docker push ${aws_ecr_repository.app_repo.repository_url}:latest
    EOF

    environment = {
      AWS_DEFAULT_REGION = var.region
    }
  }

  # Re-run the provisioner if any of these files change
  triggers = {
    dockerfile_checksum   = sha256(file("${var.app_dir}/Dockerfile"))
    app_py_checksum       = sha256(file("${var.app_dir}/app.py"))
    requirements_checksum = sha256(file("${var.app_dir}/requirements.txt"))
  }

  depends_on = [aws_iam_role_policy_attachment.apprunner_ecr_attachment, aws_ecr_repository.app_repo]
}

# Create App Runner Service
resource "aws_apprunner_service" "app_runner_service" {
  service_name = "${var.app_name}-apprunner-service"

  source_configuration {
    image_repository {
      image_identifier      = "${aws_ecr_repository.app_repo.repository_url}:latest"
      image_repository_type = "ECR"

      image_configuration {
        port = "5000"

        
      }
    }

    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_role.arn
    }
  }

  instance_configuration {
    cpu    = var.cpu    # e.g., "4096" for 4 vCPUs
    memory = var.memory # e.g., "10240" for 10 GB
  }

  tags = {
    Name = "${var.app_name}-apprunner-service"
  }

  depends_on = [null_resource.docker_build_push]
}

# (Optional) Auto Scaling Configuration
# Uncomment and configure if needed
/*
resource "aws_apprunner_auto_scaling_configuration" "auto_scaling_config" {
  name = "${var.app_name}-autoscaling-config"

  max_concurrency         = 100
  min_size                = 1
  max_size                = 10
  cpu_utilization_percentage = 70
  request_burst           = 200

  tags = {
    Name = "${var.app_name}-autoscaling-config"
  }
}

# Attach Auto Scaling Configuration to App Runner Service
resource "aws_apprunner_service" "app_runner_service" {
  # ... existing configuration ...

  auto_scaling_configuration_arn = aws_apprunner_auto_scaling_configuration.auto_scaling_config.arn

  # ... existing configuration ...
}
*/