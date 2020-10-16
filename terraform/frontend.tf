module "cdn" {
  source               = "git::https://github.com/cloudposse/terraform-aws-cloudfront-s3-cdn.git?ref=tags/0.35.0"
  dns_alias_enabled    = true
  namespace            = "luminis"
  stage                = local.stage
  name                 = "frontend"
  parent_zone_name     = var.dns_zone
  website_enabled      = true
  origin_force_destroy = true
  logging_enabled      = false

  aliases              = [
    local.app_domain_full
  ]

  acm_certificate_arn = module.certificate-frontend.arn
  tags                = local.tags
}

resource "null_resource" "frontend-sync" {
  depends_on = [module.cdn.s3_bucket]

  triggers = {
    always: timestamp()
  }

  provisioner "local-exec" {
    command = "aws s3 sync ../frontend/build s3://${module.cdn.s3_bucket}"
  }
}

output "frontend" {
  depends_on = [null_resource.frontend-sync]
  value      = "https://${local.app_domain_full}"
}
