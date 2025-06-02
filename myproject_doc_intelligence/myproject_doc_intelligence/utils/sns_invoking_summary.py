import boto3
import json
import time
from django.conf import settings
from google import genai
import os


def sns_invoking_summary():
    client = genai.Client(api_key=settings.GCP_API_KEY)
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Database_storage_for_doc_analysis")
    story = []
    while True:
        response = table.get_item(
            Key={"user_id": "anonymous", "file_name": settings.FILE_NAME}
        )
        if response:
            story = response["Item"]["lines"]
            break
        time.sleep(2)

    model_response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Please summarize the following text which is provided as lines:\n\n{story}",
    )
    print(model_response.text)
    response = table.put_item(
        Item={
            "user_id": "anonymous",
            "file_name": settings.FILE_NAME,
            "lines": story,
            "summary": model_response.text,
        }
    )
    return model_response.text
