module "certificate" {
  source                            = "git::https://github.com/cloudposse/terraform-aws-acm-request-certificate.git?ref=tags/0.7.0"
  domain_name                       = local.app_domain_full
  process_domain_validation_options = true
  zone_name                         = var.dns_zone
  ttl                               = "300"
  wait_for_certificate_issued       = true
  tags                              = local.tags

  providers = {
    aws: aws.us
  }
}
