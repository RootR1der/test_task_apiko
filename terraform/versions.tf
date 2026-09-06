terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # For production, recommend configuring remote S3 state backend with DynamoDB locking:
  # backend "s3" {
  #   bucket         = "your-terraform-state-bucket"
  #   key            = "nestjs-todo/production/terraform.tfstate"
  #   region         = "eu-central-1"
  #   dynamodb_table = "terraform-state-locks"
  #   encrypt        = true
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
