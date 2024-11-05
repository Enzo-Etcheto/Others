import json
import logging
import botocore
import boto3
from decimal import Decimal

logger = logging.getLogger('CorporateDataLogger')

#Funcion para habilitar el logger
def enable_logging():
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
class UADER_IS2_listCorporateData:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('CorporateData')
    
    def decimal_default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  
        raise TypeError  
    def listCorporateData(self, id):
            """Este método recupera todos los elementos de una tabla de DynamoDB y los devuelve como una lista. 
            Si se produce un error del cliente durante la operación, detecta la excepción y devuelve un objeto 
            JSON con un mensaje de error."""
            logger.debug("Se llama a listCorporateData, id: {id}".format(id=id))
            try:
                response = self.table.scan()
                return response.get('Items', [])
            except botocore.exceptions.ClientError as e:
                logger.error(f'Error al obtener los datos: {str(e)}')
                return json.dumps({"error": str(e)})

def main():
    site_id = "UADER-FCyT-IS2"
    list_corporate = UADER_IS2_listCorporateData()
    log_corporate = list_corporate.listCorporateData(site_id)
    log_corporate_json = json.dumps(log_corporate, indent=2, default=list_corporate.decimal_default, ensure_ascii=False)
    print("Entradas en la tabla CorporateData:\n", log_corporate_json)

if __name__ == "__main__":
    main()