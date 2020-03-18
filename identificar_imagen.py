import boto3
import json

ACCESS_KEY = '<Acces Key de AWS>'
SECRET_KEY = '<Secret Key de AWS>'

bucket = 'mlds-4-access-secure'

client = boto3.client("rekognition", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
s3_client = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Funcion para identificar una imagen entre las que existen en las colecciones

def lambda_handler(event, context):
    key = event["key"]
    download_path = "/tmp/imagen.jpeg"

    s3_client.download_file(bucket, key, download_path)
    with open(download_path, "rb") as file:
        im_bytes = file.read()
    collections = client.list_collections()

    response = buscar_matches(im_bytes, collections['CollectionIds'])

    return {
        'statusCode': 200,

        'key': key,
        'usuario': response
    }


def buscar_matches(imagen, lista_collecciones):
    encontrado = 0
    for i in lista_collecciones:
        tolerancia = 95.00
        response = client.search_faces_by_image(
            CollectionId=i,
            FaceMatchThreshold=tolerancia,
            Image={'Bytes': imagen},
            MaxFaces=1,
        )
        facematch = response['FaceMatches']
        if len(facematch) > 0:
            similitud = facematch[0]['Similarity']
            if similitud > tolerancia:
                extimgid = facematch[0]['Face']['ExternalImageId']
                encontrado = +1
                print("Antes de agregar_a_coleccion")
                agregar_a_coleccion(i, extimgid, imagen)
                usuario = {
                    'similitud': similitud,
                    'external_image_id': extimgid,
                    'coleccion': i
                }

                break

    if encontrado == 0:
        usuario = {}

    return usuario


def agregar_a_coleccion(coleccion, image_id, imagen):
    print("Agregando a coleccion...", coleccion)
    response = client.index_faces(
        CollectionId=coleccion,
        DetectionAttributes=[],
        ExternalImageId=image_id,
        Image={'Bytes': imagen},
    )




