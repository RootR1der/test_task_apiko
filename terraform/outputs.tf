# ==========================================================
# Terraform Outputs
# ==========================================================

output "alb_dns_name" {
  description = "Публічне DNS ім'я Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "app_url" {
  description = "URL для доступу до додатку та Swagger UI"
  value       = local.has_ssl_certificate ? "https://${var.domain_name}/api" : "http://${aws_lb.main.dns_name}/api"
}

output "api_healthcheck_url" {
  description = "URL для перевірки стану API"
  value       = local.has_ssl_certificate ? "https://${var.domain_name}/api/v1" : "http://${aws_lb.main.dns_name}/api/v1"
}

output "ecr_repository_url" {
  description = "URL приватного AWS ECR репозиторію для CI/CD"
  value       = aws_ecr_repository.app.repository_url
}

output "ecs_cluster_name" {
  description = "Назва кластера ECS"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "Назва сервісу ECS"
  value       = aws_ecs_service.main.name
}

output "cloudwatch_log_group" {
  description = "Назва групи логів у CloudWatch"
  value       = aws_cloudwatch_log_group.app.name
}
