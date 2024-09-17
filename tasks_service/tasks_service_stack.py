from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

class TasksServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # Define DynamoDB table for tasks
        table = dynamodb.Table(
            self, "TasksTable",
            partition_key=dynamodb.Attribute(name="taskId", type=dynamodb.AttributeType.STRING)
        )

        # Create a Lambda function for handling CRUD operations
        tasks_lambda = _lambda.Function(
            self, "TasksFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="tasks.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name,
            },
        )

        # Grant Lambda permissions to access the DynamoDB table
        table.grant_read_write_data(tasks_lambda)

        # Define API Gateway
        api = apigateway.RestApi(
            self, "TasksApi",
            rest_api_name="Tasks Service",
        )

        # Integrate Lambda with API Gateway
        tasks_integration = apigateway.LambdaIntegration(tasks_lambda)

        # Define the CRUD endpoints
        tasks_resource = api.root.add_resource("tasks")
        tasks_resource.add_method("POST", tasks_integration)  # Create Task
        tasks_resource.add_method("GET", tasks_integration)   # Get Tasks

        task_resource = tasks_resource.add_resource("{taskId}")
        task_resource.add_method("GET", tasks_integration)    # Get specific Task
        task_resource.add_method("PUT", tasks_integration)    # Update Task
        task_resource.add_method("DELETE", tasks_integration) # Delete Task  
