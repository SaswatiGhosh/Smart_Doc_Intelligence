import boto3
import json
import time
from django.conf import settings
from google import genai
import os


client = genai.Client(api_key=settings.GCP_API_KEY)
dynamodb = boto3.resource("dynamodb")
chat_history_list = []
database_storage = dynamodb.Table("Database_storage_for_doc_analysis")
chat_history = dynamodb.Table("smart_doc_chat_history")


# Populate the chat_history variable if already present in the table
def populate_chat_history():
    response = chat_history.get_item(
        Key={"user_id": "anonymous", "file_name": settings.FILE_NAME}
    )
    print(response)
    # Check if response is present and inside that chat_history is present
    if response and "Item" in response:
        chat_history_list = response["Item"]["chat_history"]


def summary_generation(response):
    summary = ""
    story = response["Item"]["lines"]
    if response["Item"]["summary"]:
        # if the summary is present then store it
        summary = response["Item"]["summary"]
    else:
        # if summary not present invoke the model
        model_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Please summarize the following text which is provided as lines:\n\n{story}",
        )

        # set the summary value
        summary = model_response.text
        print(model_response.text)

        # store the summary in the dynamoDB table
        response = database_storage.put_item(
            Item={
                "user_id": "anonymous",
                "file_name": settings.FILE_NAME,
                "lines": story,
                "summary": summary,
            }
        )

        # append the last summary in chat_history
        chat_history_list.append({"sender": "Summary", "text": model_response.text})

        # store the chat history in dynamo DB
        history_response = chat_history.put_item(
            Item={
                "user_id": "anonymous",
                "file_name": settings.FILE_NAME,
                "chat_history": chat_history_list,
            }
        )


def chat_response_generation(response, message):
    story = response["Item"]["lines"]
    # ask the model for the answer
    model_response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{message}\n\nPlease use the following text which is provided as lines for the answer:\n\n{story}\n\n Add if required in this answer but  related to the shared lines",
    )
    chat_response = model_response.text
    # append the last summary in chat_history
    chat_history_list.append({"sender": message, "text": chat_response})
    # store the chat history in dynamo DB
    history_response = chat_history.put_item(
        Item={
            "user_id": "anonymous",
            "file_name": settings.FILE_NAME,
            "chat_history": chat_history_list,
        }
    )


def sns_invoking_summary(action, message):
    populate_chat_history()
    while True:
        response = database_storage.get_item(
            Key={"user_id": "anonymous", "file_name": settings.FILE_NAME}
        )
        if response:
            break
        time.sleep(2)

    if action == "send" and message:
        chat_response_generation(response, message)
    else:
        summary_generation(response)

    return chat_history_list
