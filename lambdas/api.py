import os

from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, ProxyEventType
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

app = ApiGatewayResolver(proxy_type=ProxyEventType.APIGatewayProxyEvent)


@app.get("/error")
def get_error():
    raise Exception("Error!!")


@app.get("/hello")
def get_hello_world():
    return {"message": "hello world", "version": os.getenv("AWS_LAMBDA_FUNCTION_VERSION")}


def handler(event: APIGatewayProxyEvent, context: LambdaContext):
    return app.resolve(event, context)
