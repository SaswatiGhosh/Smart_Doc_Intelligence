import logging
import boto3
import requests
from django.conf import settings
from botocore.exceptions import ClientError


def get_presigned_upload_url(name, content_type):
    upload_url = ""

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    try:
        s3_key = f"{name}"
        print(s3_key)
        upload_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": s3_key,
                "ContentType": content_type,
            },
            ExpiresIn=3600,  # 1 hour
        )

    except ClientError as e:
        logging.error(e)
        return ""
    return upload_url


def upload_file_to_s3(file, file_name, content_type):
    presigned_url = get_presigned_upload_url(file_name, content_type)
    # file_data=file.read()
    with open(file, "rb+") as f:
        response = requests.put(
            presigned_url, data=f, headers={"Content-Type": content_type}
        )
    print(response.text)
    print(presigned_url)
    return response.status_code == 200
