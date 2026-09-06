# ==========================================================
# Security Groups (ALB and ECS Fargate Tasks)
# ==========================================================

# 1. ALB Security Group (Internet Facing)
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-${var.environment}-alb-sg"
  description = "Controls HTTP/HTTPS ingress traffic to the Application Load Balancer"
  vpc_id      = aws_vpc.main.id

  # Allow HTTP
  ingress {
    description = "Allow inbound HTTP from anywhere"
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTPS
  ingress {
    description = "Allow inbound HTTPS from anywhere"
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound to everywhere
  egress {
    description = "Allow all outbound traffic"
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-alb-sg"
  }
}

# 2. ECS Tasks Security Group (Strictly isolated)
resource "aws_security_group" "ecs_tasks" {
  name        = "${var.project_name}-${var.environment}-ecs-tasks-sg"
  description = "Allows inbound traffic ONLY from the ALB security group on container port"
  vpc_id      = aws_vpc.main.id

  # Ingress ONLY from ALB
  ingress {
    description     = "Allow traffic only from ALB security group"
    protocol        = "tcp"
    from_port       = var.container_port
    to_port         = var.container_port
    security_groups = [aws_security_group.alb.id]
  }

  # Outbound to MongoDB Atlas, ECR, CloudWatch
  egress {
    description = "Allow all outbound traffic (database, ECR, logs)"
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-ecs-tasks-sg"
  }
}
