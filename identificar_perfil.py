import boto3
import requests
import time

endpoint = '<endpoint de Azure>'
subscription_key = '<subscription key de Azure>'
ACCESS_KEY = '<Acces Key de AWS>'
SECRET_KEY = '<Secret Key de AWS>'

bucket = 'mlds-4-access-secure'
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Funcion para identificar un perfil de voz con speaker recognition de Azure a partir de una grabación en formato WAV almacenada en S3


def lambda_handler(event, context):
    # Cargamos el audio a identificar desde s3, la ruta se envia en la solicitud
    key = event["key"]
    download_path = "/tmp/audio.wav"
    s3_client.download_file(bucket, key, download_path)

    # Realizamos la identificacion
    resultado = identificar_audio(download_path)
    return resultado


def identificar_audio(file_path):
    perfiles = consultar_perfiles()
    profile_ids = [profile["identificationProfileId"] for profile in perfiles if
                   profile["enrollmentStatus"] == "Enrolled"]
    string_ids = ','.join(profile_ids)
    headers = {"Ocp-Apim-Subscription-Key": subscription_key, "Content-Type": "application/octet-stream"}
    params = {"identificationProfileIds": string_ids,
              "shortAudio": "true"}
    url = '{0}/identify'.format(endpoint)
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
            time.sleep(2)


def consultar_perfiles():
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    body = {"locale": "es-ES"}
    response = requests.get(endpoint + "/identificationProfiles", headers=headers, data=body)
    response.raise_for_status()
    perfiles = response.json()
    return perfiles


