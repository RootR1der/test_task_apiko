# ==========================================================
# Amazon CloudWatch Logs Group
# ==========================================================

resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${var.project_name}-${var.environment}"
  retention_in_days = var.log_retention_in_days

  tags = {
    Name = "${var.project_name}-${var.environment}-logs"
  }
}
