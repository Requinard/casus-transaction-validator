resource "aws_api_gateway_domain_name" "record" {
  domain_name     = local.app_domain_full
  certificate_arn = module.certificate.arn
}

resource "aws_api_gateway_base_path_mapping" "record" {
  api_id      = aws_api_gateway_rest_api.app.id
  domain_name = aws_api_gateway_domain_name.record.domain_name
  stage_name  = aws_api_gateway_deployment.app.stage_name
}

resource "aws_route53_record" "record" {
  name    = local.app_domain
  type    = "A"
  zone_id = data.aws_route53_zone.base_zone.id

  alias {
    evaluate_target_health = true
    name                   = aws_api_gateway_domain_name.record.cloudfront_domain_name
    zone_id                = aws_api_gateway_domain_name.record.cloudfront_zone_id
  }
}

output "api_friendly_url" {
  value = "https://${aws_api_gateway_domain_name.record.domain_name}"
}
