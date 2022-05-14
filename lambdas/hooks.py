import json

import boto3

STATUS_SUCCEEDED = "Succeeded"
codedeploy = boto3.client("codedeploy")


def pre_hook_handler(event, context):
    print(json.dumps(event))
    # {
    #     "DeploymentId": "d-XXXXXXXXX",
    #     "LifecycleEventHookExecutionId": "xxxxxxxxxxxxxxxxxxxxxxxx"
    # }
    print("デプロイ開始したよ！")
    codedeploy.put_lifecycle_event_hook_execution_status(
        deploymentId=event["DeploymentId"],
        lifecycleEventHookExecutionId=event["LifecycleEventHookExecutionId"],
        status=STATUS_SUCCEEDED,
    )


def post_hook_handler(event, context):
    print(json.dumps(event))
    # {
    #     "DeploymentId": "d-XXXXXXXXX",
    #     "LifecycleEventHookExecutionId": "xxxxxxxxxxxxxxxxxxxxxxxx"
    # }
    print("デプロイ終わったよ！")
    codedeploy.put_lifecycle_event_hook_execution_status(
        deploymentId=event["DeploymentId"],
        lifecycleEventHookExecutionId=event["LifecycleEventHookExecutionId"],
        status=STATUS_SUCCEEDED,
    )
