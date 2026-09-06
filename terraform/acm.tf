# ==========================================================
# AWS Certificate Manager (ACM) & SSL Configuration
# ==========================================================

locals {
  # Check if custom domain or certificate was provided
  has_custom_domain   = var.domain_name != ""
  has_existing_cert   = var.certificate_arn != ""
  has_ssl_certificate = local.has_existing_cert || local.has_custom_domain

  # Determine which certificate ARN to use
  certificate_arn = local.has_existing_cert ? var.certificate_arn : (
    local.has_custom_domain ? aws_acm_certificate.cert[0].arn : ""
  )
}

# Optional: Request ACM Certificate if domain_name is specified
resource "aws_acm_certificate" "cert" {
  count             = local.has_custom_domain && !local.has_existing_cert ? 1 : 0
  domain_name       = var.domain_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-acm-cert"
  }
}
