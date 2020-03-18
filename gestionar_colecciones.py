import boto3
import json

ACCESS_KEY = '<Acces Key de AWS>'
SECRET_KEY = '<Secret Key de AWS>'

bucket = 'mlds-4-access-secure'

client = boto3.client("rekognition", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
s3_client = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# funcion para gestionar colecciones disponibles


def lambda_handler(event, context):
    response = ''
    if event.get("borrar") is None:
        pass
    else:
        response = client.delete_collection(CollectionId=event.get("borrar"))

    colecciones = client.list_collections()
    return {
        'statusCode': 200,
        'colecciones': colecciones['CollectionIds'],
        'response': response
    }
