module "certificate" {
  source                      = "git::https://github.com/cloudposse/terraform-aws-acm-request-certificate.git?ref=tags/0.7.0"
  domain_name                 = local.api_domain
  zone_name                   = var.dns_zone
  ttl                         = "300"
  wait_for_certificate_issued = true
  tags                        = local.tags

  providers = {
    aws: aws.us
  }
}

module "certificate-frontend" {
  # For some reason this module does not like alternative domain names anymore. I don't think it's 0.13 compatible
  source                      = "git::https://github.com/cloudposse/terraform-aws-acm-request-certificate.git?ref=tags/0.7.0"
  domain_name                 = local.app_domain_full
  zone_name                   = var.dns_zone
  ttl                         = "300"
  wait_for_certificate_issued = true
  tags                        = local.tags

  providers = {
    aws: aws.us
  }
}
