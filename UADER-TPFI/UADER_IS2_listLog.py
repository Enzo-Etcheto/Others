import boto3
from boto3.dynamodb.conditions import Key
import json
import botocore
import uuid
from Components.CorporateLog import CorporateLog
from Components.Log import Log

class UADER_IS2_listLog:
    def __init__(self):
            self.dynamodb = boto3.resource('dynamodb')
            self.table = self.dynamodb.Table('CorporateLog')
    def listCorporateLog(self):
            """Este fragmento de código define un método llamado listCorporateLog que toma un parámetro uuid_CPU.
            Dentro del método, intenta recuperar una tabla denominada 'CorporateLog' de un recurso de DynamoDB. 
            Luego, escanea la tabla y recupera todos los elementos.Si la operación tiene éxito, devuelve la 
            lista de elementos. Si hay un error, detecta la excepción ClientError y devuelve un objeto JSON 
            con el mensaje de error."""
            try:
                response = self.table.scan()
                return response.get('Items', [])
            except botocore.exceptions.ClientError as e:
                return json.dumps({"error": str(e)})


def main():
    log_listLog = UADER_IS2_listLog()
    log_list = log_listLog.listCorporateLog()
    print("Entradas en la tabla CorporateLog:", log_list)


if __name__ == "__main__":  
    main()