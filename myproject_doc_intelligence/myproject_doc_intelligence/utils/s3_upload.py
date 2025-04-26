import logging
import boto3
from django.conf import settings
from botocore.exceptions import ClientError


def upload_file_to_s3(file, name, content_type) -> bool:

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    try:
        response = s3_client.upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            name,
            ExtraArgs={"ContentType": content_type},
        )
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True
