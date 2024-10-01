# outputs.tf

output "app_runner_service_url" {
  description = "The URL of the App Runner service"
  value       = aws_apprunner_service.app_runner_service.service_url
}

output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.app_repo.repository_url
}
