data "aws_route53_zone" "base_zone" {
  name = var.dns_zone
}
