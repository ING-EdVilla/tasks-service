import json
import uuid
import os
import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    http_method = event['httpMethod']
    if http_method == 'POST':
        return create_task(event)
    elif http_method == 'GET':
        params = event.get('pathParameters', {})
        if params and 'taskId' in params:
            return get_task(event)
        else:
            return get_tasks(event)
    elif http_method == 'PUT':
        return update_task(event)
    elif http_method == 'DELETE':
        return delete_task(event)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'message': 'Method Not Allowed'})
        }

def create_task(event):
    body = json.loads(event['body'])
    # get a unique task id
    task_id = str(uuid.uuid4())
    task = {
        'taskId': task_id,
        'title': body.get('title', ''),
        'description': body.get('description', ''),
        'status': body.get('status', 'pending')
    }
    table.put_item(Item=task)
    return {
        'statusCode': 201,
        'body': json.dumps(task)
    }

def get_tasks(event):
    response = table.scan()
    tasks = response.get('Items', [])
    return {
        'statusCode': 200,
        'body': json.dumps(tasks)
    }

def get_task(event):
    task_id = event['pathParameters']['taskId']
    response = table.get_item(Key={'taskId': task_id})
    task = response.get('Item')
    if task:
        return {
            'statusCode': 200,
            'body': json.dumps(task)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Task not found'})
        }

def update_task(event):
    try:
        task_id = event['pathParameters']['taskId']
        # verify if exists task
        response = table.get_item(Key={'taskId': task_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Task not found'})
            }

        body = json.loads(event['body'])
        update_expression = "SET title=:t, description=:d, #st=:s"
        expression_values = {
            ':t': body.get('title', ''),
            ':d': body.get('description', ''),
            ':s': body.get('status', 'pending')
        }

        expression_attribute_names = {
            '#st': 'status'
        }

        response = table.update_item(
            Key={'taskId': task_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="ALL_NEW"
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Task updated',
                'updatedTask': response['Attributes']  # Devolvemos la tarea actualizada
            })
        }
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Internal server error',
                'error': str(e)
            })
        }

def delete_task(event):
    try:
        task_id = event['pathParameters']['taskId']
        # verify if exists task
        response = table.get_item(Key={'taskId': task_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Task not found'})
            }
            
        table.delete_item(Key={'taskId': task_id})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Task deleted'})
        }
    
    except Exception as e:
        # Manejo de excepciones y errores
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Internal server error',
                'error': str(e)
            })
        }
