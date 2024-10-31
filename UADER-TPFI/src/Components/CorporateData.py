import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import botocore
import logging
from decimal import Decimal
from Components.CorporateLog import CorporateLog

#Configuración del logger
logger = logging.getLogger('CorporateDataLogger')

#Funcion para habilitar el logger
def enable_logging():
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

class CorporateData:
    _instance = None

    @staticmethod
    def getInstance():
        if CorporateData._instance is None:
            CorporateData._instance = CorporateData()
        return CorporateData._instance

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('CorporateData')
        logger.debug("Se inicializa la clase CorporateData")


    def getData(self, uuid, uuidCPU, id):
        """Este es un método llamado getData que recupera un elemento de una tabla de DynamoDB.
          Se necesitan tres parámetros: uuid, uuidCPU e id."""
        logger.debug("Se llama a getData, uuid: {uuid}, uuidCPU: {uuidCPU}, id: {id}".format(uuid=uuid, uuidCPU=uuidCPU, id=id))
        print("Se llama a getData, uuid: {uuid}, uuidCPU: {uuidCPU}, id: {id}".format(uuid=uuid, uuidCPU=uuidCPU, id=id))
        
        try:
            response = self.table.get_item(
                Key={'id': id}
            )
            item = response.get('Item')
            if not item:
                return json.dumps({"error": "Registro no encontrado"})
            
            return json.dumps({
                "sede": item.get('sede'),
                "domicilio": item.get('domicilio'),
                "localidad": item.get('localidad'),
                "provincia": item.get('provincia')
            })
        except botocore.exceptions.ClientError as e:
            logger.error(f'Error al obtener los datos:{str(e)}')
            return json.dumps({"error": str(e)})

    def getCUIT(self, uuid, uuidCPU, id):
        """Este es un método llamado getCUIT que recupera un elemento de una tabla de DynamoDB utilizando 
        la identificación como clave principal. Luego extrae los valores "sede" y "CUIT" del elemento y 
        los devuelve como un objeto JSON. Si no se encuentra el elemento o se produce un error, 
        devuelve un objeto JSON con un mensaje de error."""
        logger.debug("Se llama a getCUIT, uuid: {uuid}, uuidCPU: {uuidCPU}, id: {id}".format(uuid=uuid, uuidCPU=uuidCPU, id=id))
        print("Se llama a getCUIT, uuid: {uuid}, uuidCPU: {uuidCPU}, id: {id}".format(uuid=uuid, uuidCPU=uuidCPU, id=id))

        try:
            response = self.table.get_item(
                Key={
                    'id': id  
                }
            )
            item = response.get('Item')
            if item:
                return json.dumps({
                    "sede": item.get('sede'),
                    "CUIT": item.get('CUIT')
                })
            else:
                logger.error("CUIT no encontrado")
                return json.dumps({"error": "CUIT no encontrado"})
        except botocore.exceptions.ClientError as e:
            logger.error(f'Error al obtener los datos:{str(e)}')
            return json.dumps({"error": str(e)})

    def getSeqID(self, uuid, uuidCPU, id):
        """Este es un método llamado getSeqID que recupera e incrementa un ID de secuencia (idSeq) 
        de una tabla de DynamoDB. Se necesitan tres parámetros: uuid, uuidCPU e id."""
        logger.debug("Se llama a getSeqID, uuid: {uuid}, uuidCPU: {uuidCPU}, id: {id}".format(uuid=uuid, uuidCPU=uuidCPU, id=id))
        print("Se llama a getSeqID, uuid: {uuid}, uuidCPU: {uuidCPU}, id: {id}".format(uuid=uuid, uuidCPU=uuidCPU, id=id))

        try:
            response = self.table.get_item(
                Key={
                    'id': id  
                }
            )
            item = response.get('Item')
            if item and 'idSeq' in item:
                new_idSeq = int(item['idSeq']) + 1
                self.table.update_item(
                    Key={'id': id},
                    UpdateExpression="SET idSeq = :val",
                    ExpressionAttributeValues={':val': Decimal(new_idSeq)},
                    ReturnValues="UPDATED_NEW"
                )
                return json.dumps({"idSeq": new_idSeq})
            else:
                logger.debug("idSeq no encontrado")
                return json.dumps({"error": "idSeq no encontrado"})
        except botocore.exceptions.ClientError as e:
            logger.error(f'Error al obtener los datos:{str(e)}')
            return json.dumps({"error": str(e)})
        
    
    @staticmethod
    def decimal_default(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError
    
    def listCorporateData(self, id):
        """Este método recupera todos los elementos de una tabla de DynamoDB y los devuelve como una lista. 
        Si se produce un error del cliente durante la operación, detecta la excepción y devuelve un objeto 
        JSON con un mensaje de error."""
        logger.debug("Se llama a listCorporateData, id: {id}".format(id=id))
        
        try:
            response = self.table.query(
                KeyConditionExpression=Key('id').eq(id)
            )
            items = response.get('Items', [])
            
            for item in items:
                print(f"Entrada:\n{json.dumps(item, indent=2, default=self.decimal_default, ensure_ascii=False)}\n")
            
            return True
        except botocore.exceptions.ClientError as e:
            logger.error(f'Error al obtener los datos: {str(e)}')
            return json.dumps({"error": str(e)})
               
    def listCorporateLog(self, uuid_CPU):
        """Este fragmento de código define un método llamado listCorporateLog que toma un parámetro uuid_CPU.
        Dentro del método, intenta recuperar una tabla denominada 'CorporateLog' de un recurso de DynamoDB. 
        Luego, escanea la tabla y recupera todos los elementos.Si la operación tiene éxito, devuelve la 
        lista de elementos. Si hay un error, detecta la excepción ClientError y devuelve un objeto JSON 
        con el mensaje de error."""
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('CorporateLog')
        logger.debug("Se llama a listCorporateLog, uuid_CPU: {uuid_CPU}".format(uuid_CPU=uuid_CPU))
        try:
            response = self.table.scan(
                 FilterExpression=Attr('CPUid').eq(uuid_CPU)
            )
            items = response.get('Items', [])
        
            for item in items:
                print(f"Entrada:\n{json.dumps(item, indent=2, default=self.decimal_default, ensure_ascii=False)}\n")
                
            return True
        except botocore.exceptions.ClientError as e:
            logger.error(f'Error al obtener los datos: {str(e)}')
            return json.dumps({"error": str(e)})
