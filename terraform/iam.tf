resource "aws_iam_role" "lambda" {
  name               = "luminis-validator-${local.stage}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy" "lambda" {
  policy = data.aws_iam_policy_document.lambda_role.json
  role   = aws_iam_role.lambda.id
}
