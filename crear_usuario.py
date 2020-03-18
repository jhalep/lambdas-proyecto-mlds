import boto3
import json

ACCESS_KEY = '<Acces Key de AWS>'
SECRET_KEY = '<Secret Key de AWS>'

bucket = 'mlds-4-access-secure'
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
usuarios_path = "/tmp/usuarios.json"


def lambda_handler(event, context):
    s3_client.download_file(bucket, 'usuarios.json', usuarios_path)
    with open(usuarios_path, "r+") as file:
        data = json.load(file)

        if event.get("usuario") is None:
            pass
        else:
            data["usuarios"].append(event)

        # data["usuarios"] = []
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    s3_client.upload_file(usuarios_path, bucket, 'usuarios.json')

    return {
        'statusCode': 200,
        'data': data
    }
