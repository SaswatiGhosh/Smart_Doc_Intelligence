import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Database_storage_for_doc_analysis")

response = table.get_item(Key={"user_id": "anonymous"})

item = response.get("Item")
print(item)
