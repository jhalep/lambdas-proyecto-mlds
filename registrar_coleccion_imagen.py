import boto3
import json

ACCESS_KEY = '<Acces Key de AWS>'
SECRET_KEY = '<Secret Key de AWS>'

bucket = 'mlds-4-access-secure'

client = boto3.client("rekognition", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
s3_client = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Crear una nueva colección y agregar una imagen


def lambda_handler(event, context):
    key = event["key"]
    image_id = event["image_id"]
    collection_name = event["collection_name"]
    download_path = "/tmp/imagen.jpeg"
    collection_response = client.create_collection(CollectionId=collection_name)

    s3_client.download_file(bucket, key, download_path)
    with open(download_path, "rb") as file:
        im_bytes = file.read()

    response = client.index_faces(
        CollectionId=collection_name,
        DetectionAttributes=[],
        ExternalImageId=image_id,
        Image={'Bytes': im_bytes}
    )

    collections = client.list_collections()
    return {
        'statusCode': 200,
        'collection_name': collection_name,
        'body': response
    }
