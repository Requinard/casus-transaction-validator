variable "dns_zone" {
  default = "aws.subjectreview.eu"
}

locals {
  stage         = terraform.workspace
  is_production = local.stage == "master"

  app_domain      = local.is_production ? "casus-validator" : "casus-validator.${local.stage}"
  app_domain_full = "${local.app_domain}.${var.dns_zone}"
  api_domain      = "api.${local.app_domain_full}"

  app_name = "casus-validator-${local.stage}"

  tags = {
    ApplicationName = "transaction-validator"
    UnitName        = "technical-case"
    Name            = "transaction-validator"
    Workspace       = terraform.workspace
    ManagedBy       = "Terraform"
    Terraform       = true
  }
}
