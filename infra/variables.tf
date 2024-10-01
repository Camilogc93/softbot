# variables.tf

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Name of the application"
  type        = string
}

variable "app_dir" {
  description = "Path to the application directory containing Dockerfile and code"
  type        = string
  default     = "./slack_logic"  # Replace 'your_app' with your actual app directory name
}

variable "cpu" {
  description = "CPU units for App Runner instance (1024 units = 1 vCPU)"
  type        = string
  default     = "1024"  # 4 vCPUs
}

variable "memory" {
  description = "Memory for App Runner instance in MiB"
  type        = string
  default     = "2048"  # 10 GB
}
