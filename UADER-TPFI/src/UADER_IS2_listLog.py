import boto3
from boto3.dynamodb.conditions import Key
import json
import botocore
import logging
from decimal import Decimal
from Components.CorporateLog import CorporateLog
from Components.Log import Log

#Configuración del logger
logger = logging.getLogger('CorporateDataLogger')

#Funcion para habilitar el logger
def enable_logging():
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
class UADER_IS2_listLog:
    def __init__(self):
            self.dynamodb = boto3.resource('dynamodb')
            self.table = self.dynamodb.Table('CorporateLog')
    
    def decimal_default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  
        raise TypeError  
    def listCorporateLog(self):
            """Este fragmento de código define un método llamado listCorporateLog que toma un parámetro uuid_CPU.
            Dentro del método, intenta recuperar una tabla denominada 'CorporateLog' de un recurso de DynamoDB. 
            Luego, escanea la tabla y recupera todos los elementos.Si la operación tiene éxito, devuelve la 
            lista de elementos. Si hay un error, detecta la excepción ClientError y devuelve un objeto JSON 
            con el mensaje de error."""
            logger.debug("Se llama a listCorporateLog")
            try:
                response = self.table.scan()
                return response.get('Items', [])
            except botocore.exceptions.ClientError as e:
                logger.error(f'Error al obtener los datos: {str(e)}')
                return json.dumps({"error": str(e)})


def main():
    log_listLog = UADER_IS2_listLog()
    log_list = log_listLog.listCorporateLog()
    log_list_json = json.dumps(log_list, indent=2, ensure_ascii=False, default=log_listLog.decimal_default)
    print("Entradas en la tabla CorporateLog:\n", log_list_json)


if __name__ == "__main__":  
    main()