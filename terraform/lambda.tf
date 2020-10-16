module "lambda_function" {
  source = "git::https://gitea.mail.requinard.nl/requinard/terraform-modules.git//lambda-framework-apigateway?ref=master"

  dns_certificate_arn = module.certificate.arn
  dns_full_domain     = local.api_domain
  dns_zone_id         = data.aws_route53_zone.base_zone.id

  lambda_handler = "lambda.handler"
  lambda_name    = "luminis-transaction-validator-${local.stage}"
  lambda_runtime = "python3.8"
  lambda_zip     = "../app.zip"
}

output "api_friendly_url" {
  value = module.lambda_function.friendly_invoke_url
}
