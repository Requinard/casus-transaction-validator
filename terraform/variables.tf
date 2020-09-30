variable "dns_zone" {
  default = "aws.subjectreview.eu"
}

locals {
  stage           = terraform.workspace
  app_domain      = local.stage == "production" ? "luminis-validator" : "luminis-validator.${local.stage}"
  app_domain_full = "${local.app_domain}.${var.dns_zone}"

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
