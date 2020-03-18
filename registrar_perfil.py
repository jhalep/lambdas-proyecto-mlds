import boto3
import requests
import time

endpoint = '<endpoint de Azure>'
subscription_key = '<subscription key de Azure>'
ACCESS_KEY = '<Acces Key de AWS>'
SECRET_KEY = '<Secret Key de AWS>'

bucket = 'mlds-4-access-secure'
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Funcion para registrar un perfil de voz con speaker recognition de Azure a partir de una grabación en formato WAV almacenada en S3


def lambda_handler(event, context):
    key = event["key"]
    download_path = "/tmp/audio.wav"
    perfil_id = crear_perfil()
    s3_client.download_file(bucket, key, download_path)
    resultado = crear_enrollment(perfil_id, download_path)
    return {
        'statusCode': 200,
        'key': event["key"],
        'perfil_id': perfil_id,
        'resultado': resultado
    }


def crear_perfil():
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    body = {"locale": "es-ES"}
    response = requests.post(endpoint + "/identificationProfiles", headers=headers, data=body)
    response.raise_for_status()
    create_results = response.json()
    return create_results["identificationProfileId"]


def crear_enrollment(profile_id, file_path):
    headers = {"Ocp-Apim-Subscription-Key": subscription_key, "Content-Type": "application/octet-stream"}
    params = {"shortAudio": "true"}
    url = '{0}/identificationProfiles/{1}/enroll'.format(endpoint, profile_id)
    with open(file_path, 'rb') as data:
        response = requests.post(url, headers=headers, params=params, data=data)
        operation_status_url = response.headers["Operation-Location"]
        respuesta = verificar_estado_operacion(operation_status_url)
        return respuesta


def verificar_estado_operacion(url):
    headers = {"Ocp-Apim-Subscription-Key": subscription_key, "Content-Type": "application/json"}
    while True:
        print("Verificando usuario...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        body = response.json()
        if body["status"] == "succeeded":
            return body
        elif body["status"] == "failed":
            return body
        else:
            time.sleep(1)
