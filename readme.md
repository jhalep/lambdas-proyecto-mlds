## Funciones Lambda Proyecto final MDLS-4

### Descripción

Scripts de funciones lambda para creación de perfiles de voz e imagen para posterior identificación

- El registro e identificación de perfiles de audio se realiza con las  [APIs de Azure Speaker recognition](https://westus.dev.cognitive.microsoft.com/docs/services/563309b6778daf02acc0a508/operations/5645c3271984551c84ec6797)

- El registro e identificación de perfiles de imagen se realiza con [Rekognition](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Client.search_faces_by_image) de AWS

- Las Funciones de identificación y registro reciben como parámetro en el body del request el key de la ubicación del archivo en el bucket de S3

