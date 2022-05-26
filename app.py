import os

import aws_cdk as cdk
from aws_cdk import aws_apigateway, aws_cloudwatch, aws_codedeploy, aws_lambda

app = cdk.App()
stack = cdk.Stack(app, "test")

# 0. 変数的なもの

# LambdaPowertools
LAMBDA_POWERTOOLS_LAYER_ARN = (
    f"arn:aws:lambda:{os.getenv('CDK_DEFAULT_REGION')}:017000801446:layer:AWSLambdaPowertoolsPython:3"
)
# Lambdaの共有設定
FN_PARAM = dict(
    code=aws_lambda.Code.from_asset("lambdas"),
    runtime=aws_lambda.Runtime.PYTHON_3_9,
)

# 1. Lambda関数を作成する

powertools_layer = aws_lambda.LayerVersion.from_layer_version_arn(
    stack, "powertoolsLayer", LAMBDA_POWERTOOLS_LAYER_ARN
)
function = aws_lambda.Function(stack, "Function", handler="api.handler", layers=[powertools_layer], **FN_PARAM)

# 2. Lambdaのエイリアスをホストする

version = function.current_version
alias = aws_lambda.Alias(stack, "Alias", alias_name="hogehoge", version=version)
aws_apigateway.LambdaRestApi(stack, "Api", handler=alias)

# 3. エイリアスをカナリアデプロイさせる

# 3-1. CodeDeployを作成する
# アプリケーションを作る
application = aws_codedeploy.LambdaApplication(stack, "Application")
deployment_group = aws_codedeploy.LambdaDeploymentGroup(
    stack,
    "CanariaDeploy",
    application=application,
    alias=alias,
    deployment_config=aws_codedeploy.LambdaDeploymentConfig.CANARY_10_PERCENT_5_MINUTES
)

# 3-2. デプロイ中にエラーが発生した場合にロールバックさせる
alarm = aws_cloudwatch.Alarm(
    stack,
    "Alarm",
    comparison_operator=aws_cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
    threshold=1,
    evaluation_periods=1,
    metric=alias.metric_errors(),
)
deployment_group.add_alarm(alarm)

app.synth()
