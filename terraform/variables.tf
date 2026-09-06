variable "aws_region" {
  description = "AWS регіон для розгортання інфраструктури"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Назва проекту для іменування та тегування ресурсів"
  type        = string
  default     = "nestjs-todo"
}

variable "environment" {
  description = "Середовище розгортання (production, staging, dev)"
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "CIDR блок для VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnets" {
  description = "CIDR блоки для публічних підмереж (мінімум 2 у різних AZ для ALB)"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnets" {
  description = "CIDR блоки для приватних підмереж (для безпечного запуску ECS Fargate)"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "container_port" {
  description = "Порт, на якому працює NestJS додаток всередині контейнера"
  type        = number
  default     = 3000
}

variable "app_count" {
  description = "Кількість реплік (tasks) ECS додатку для забезпечення High Availability"
  type        = number
  default     = 2
}

variable "fargate_cpu" {
  description = "Обчислювальні одиниці vCPU для Fargate task (256 = 0.25 vCPU)"
  type        = number
  default     = 256
}

variable "fargate_memory" {
  description = "Об'єм оперативної пам'яті в MB для Fargate task (512 = 0.5 GB)"
  type        = number
  default     = 512
}

variable "app_image" {
  description = "URI Docker образу для первинного запуску (пізніше оновлюється через CI/CD)"
  type        = string
  default     = "" # Якщо порожньо, використовується створений ECR репозиторій з тагом latest
}

variable "database_uri" {
  description = "Connection string до MongoDB (наприклад, MongoDB Atlas)"
  type        = string
  sensitive   = true
  default     = "mongodb+srv://user:password@cluster0.mongodb.net/notes_todo?retryWrites=true&w=majority"
}

variable "domain_name" {
  description = "Власне доменне ім'я (наприклад, api.mycompany.com). Якщо вказано, генерується ACM сертифікат"
  type        = string
  default     = ""
}

variable "certificate_arn" {
  description = "Існуючий ARN сертифіката ACM для HTTPS (якщо створено заздалегідь)"
  type        = string
  default     = ""
}

variable "enable_nat_gateway" {
  description = "Створювати NAT Gateway для приватних підмереж. Для production рекомендується true. Для дешевого тестування можна вимкнути (false)"
  type        = bool
  default     = true
}

variable "log_retention_in_days" {
  description = "Термін зберігання логів у CloudWatch (у днях)"
  type        = number
  default     = 14
}
