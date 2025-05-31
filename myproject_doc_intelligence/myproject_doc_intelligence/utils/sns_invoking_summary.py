import boto3
import json
import time
from django.conf import settings
import google.generativeai as genai
import os


def sns_invoking_summary():
    genai.configure(api_key=settings.GCP_API_KEY)
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Database_storage_for_doc_analysis")
    story = []
    while True:
        response = table.get_item(
            Key={"user_id": "anonymous", "file_name": settings.FILE_NAME}
        )
        story = response["Item"]["lines"]
        if story:
            break
        time.sleep(2)
    model = genai.GenerativeModel("gemini-1.5-flash")
    model_response = model.generate_content(
        [f"Please summarize the following text which is provided as lines:\n\n{story}"]
    )
    response = table.put_item(
        Item={
            "user_id": "anonymous",
            "file_name": settings.FILE_NAME,
            "lines": story,
            "summary": model_response.text,
        }
    )
    return model_response.text
