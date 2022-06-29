
### Sessions API

#### Useful Links
[Introduction to FastAPI and Local DynamoDB
](https://medium.com/nerd-for-tech/introduction-to-fastapi-and-local-dynamodb-595c990ed0f8)
[Python FastAPI with AWS DynamoDB
](https://medium.com/nerd-for-tech/python-fastapi-with-aws-dynamodb-931073a87a52)
[Figma Multiplayer session syncing](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)
[FastAPI App to Production AWS](https://medium.com/aws-tip/taking-a-fastapi-app-to-production-on-aws-189ebf3defed)

#### Development Notes
- Start API - `uvicorn app.main:app --reload --port 5000`

#### DynamoDB
- region: `us-east-1`
- standard endpoint for region: `ENDPOINT_URL=https://dynamodb.us-east-1.amazonaws.com`
- DynamoDB is deployed to AWS via managed service, service account `sessions-api-service` is used.
