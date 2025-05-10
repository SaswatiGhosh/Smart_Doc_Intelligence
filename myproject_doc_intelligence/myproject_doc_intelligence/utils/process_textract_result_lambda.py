import json
import boto3
import logging
import re

logger = logging.getLogger()

textract=boto3.client('textract')
def lambda_handler(event, context):
    print("Recieved SNS notification", json.dumps(event))
    print(event)
#Extract JobID from SNS
    
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info(f"Message: {message}")
    job_id = message['JobId']
    status = message['Status']
    file_name =message['DocumentLocation']['S3ObjectName']
    print(file_name)

    print(f"Textract job {job_id} | Status ID {status}")

    if status !="SUCCEEDED":
        print("Textract failed job or was not successful")
        return {
            'statusCode' : 400,
            'body': json.dumps('Textract job failed or incomplete.')
        }
    #Get textract result
    response=textract.get_document_analysis(JobId=job_id)
    blocks=response.get('Blocks',[])

    #extracted text to be displayed
    extracted_lines=[ block['Text'] for block in blocks if block['BlockType']=='LINE']

    print('Extracted lines')
    extracted_lines = clean_lines(extracted_lines)

    print(extracted_lines)

    stored_lines=store_lines_in_dynamoDB(extracted_lines, file_name)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Textract results processed',
            'lines': extracted_lines
        })
    }

    
def clean_lines(extracted_lines):
    clean_lines = [line.strip() for line in extracted_lines]
    clean_lines = [re.sub(r'\s+', ' ', line) for line in clean_lines]
    # clean_lines =[re.sub(r'[^\x00-\x7f]+', '' , clean_lines)]
    return clean_lines


def store_lines_in_dynamoDB(lines,file_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Database_storage_for_analysis')
    response=table.put_item(Item={'user_id': "anonymous",'file_name': file_name,'lines': lines, 'summary' : ""})
    print("Stored lines in DynamoDB")


    