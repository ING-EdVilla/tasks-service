# Serverless Tasks Service API

This project sets up a serverless CRUD API for managing tasks using AWS CDK, AWS Lambda, API Gateway, and DynamoDB.

## Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/)
- [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk.html)
- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) (for CDK)
- [pip](https://pip.pypa.io/en/stable/) (Python package installer)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ING-EdVilla/tasks-service.git
cd tasks-service
```
python -m venv .env
source .env/bin/activate  # On Windows, use `.env\Scripts\activate`
pip install -r requirements.txt
npm install -g aws-cdk
aws configure (Make sure your AWS credentials are configured.)
cdk bootstrap (Initialize your CDK environment)
cdk deploy (Deploy the stack)

This will create the necessary resources on AWS, such as Lambda functions, API Gateway, and DynamoDB tables.

## Running the Project

To test your API, use the endpoint provided by API Gateway after deploying the stack with CDK. You can use tools like curl, Postman, or any HTTP client to make requests to the following endpoints:

POST /tasks - Create a new task
GET /tasks - Retrieve all tasks
GET /tasks/{taskId} - Retrieve a specific task by ID
PUT /tasks/{taskId} - Update a specific task by ID
DELETE /tasks/{taskId} - Delete a specific task by ID

You can also try the API with my implementation: https://b4cz76pshl.execute-api.us-east-1.amazonaws.com/prod/
