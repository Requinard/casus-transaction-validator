resource "aws_iam_role" "lambda" {
  name               = "luminis-validator-${local.stage}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}
