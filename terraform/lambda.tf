resource "aws_lambda_function" "lambda" {
  function_name    = "luminis-transaction-validator-${local.stage}"
  filename         = "../app.zip"
  handler          = "api.handler"
  role             = aws_iam_role.lambda.arn
  runtime          = "python3.8"
  source_code_hash = filebase64sha256("../app.zip")
}

resource "aws_lambda_permission" "apigateway" {
  action        = "lambda:InvokeFunction"
  statement_id  = "ApiGatewayInvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.app.execution_arn}/*/*"
}
