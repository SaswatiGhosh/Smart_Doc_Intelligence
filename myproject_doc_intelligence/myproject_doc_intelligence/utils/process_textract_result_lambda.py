import json
import boto3


textract=boto3.client('textract')
def lambda_handler(event, context):
    print("Recieved SNS notification", json.dump(event))

#Extract JobID from SNS
    message=json.loads(event['Records'][0]['sns']['message'])
    job_id = message['JobId']
    status = message['Status']

    print(f"Textract job {job_id} | Status ID {status}")

    if status !="SUCCEEDED":
        print("Textract failed job or was not successful")
        return {
            'statusCode' : 400,
            'body': json.dumps('Textract job failed or incomplete.')
        }
    #Get textract result
    response=textract.get_document_analysis(JobID=job_id)
    blocks=response.get('Blocks',[])

    #extracted text to be displayed
    extracted_lines=[ block['Text'] for block in blocks if ['BlockType']=='LINE']

    print('Extracted lines')

    for line in extracted_lines:
        print(line)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Textract results processed',
            'lines': extracted_lines
        })
    }