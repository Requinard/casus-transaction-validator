variable "dns_zone" {
  default = "aws.subjectreview.eu"
}

locals {
  stage         = terraform.workspace
  is_production = local.stage == "master"

  app_domain      = local.is_production ? "luminis-validator" : "luminis-validator.${local.stage}"
  app_domain_full = "${local.app_domain}.${var.dns_zone}"
  api_domain      = "api.${local.app_domain_full}"

  app_name = "luminis-validator-${local.stage}"

  tags = {
    ApplicationName = "transaction-validator"
    UnitName        = "luminis"
    Name            = "transaction-validator"
    Workspace       = terraform.workspace
    ManagedBy       = "Terraform"
    Terraform       = true
  }
}
