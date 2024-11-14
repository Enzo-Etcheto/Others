import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr
import uuid as uuid
import datetime
import logging  
import json
from decimal import Decimal
from botocore.exceptions import ClientError

#Configuración del logger
logger = logging.getLogger('CorporateLogLogger')

#Función para habilitar el logger
def enable_logging():
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
class Log:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('CorporateLog')

    def post(self, uuid_session, method_name):
        """Este es un método llamado post que registra un evento en una tabla de DynamoDB. 
        Crea un elemento de registro con un ID único, un ID de sesión, un ID de CPU, un nombre de método
        y una marca de tiempo, y luego intenta agregarlo a la tabla. Si tiene éxito, imprime un mensaje 
        de éxito; de lo contrario, detecta el error e imprime un mensaje de error."""
        timestamp = datetime.datetime.now().isoformat()
        cpu_id = uuid.getnode() 
        uniqueID=str(uuid.uuid4())

        log_item = {
            'id': uniqueID,
            'session_id': uuid_session,
            'CPUid': cpu_id,
            'method': method_name,
            'timestamp': timestamp
        }

        try:
            self.table.put_item(Item=log_item)
            log_item_json = json.dumps(log_item, indent=2, ensure_ascii=False)
            logger.debug(f"Operación registrada en el log: {log_item_json}")
            print(f"Operación registrada en el log: {log_item_json}")
        except botocore.exceptions.ClientError as e:
            logger.error(f"Error al registrar en el log: {e.response['Error']['Message']}")
            print(f"Error al registrar en el log: {e.response['Error']['Message']}")
        
    def list(self, uuid_cpu, uuid=None):
        logger.debug("Se llama a list, uuid_cpu: {uuid_cpu}, uuid: {uuid}".format(uuid_cpu=uuid_cpu, uuid=uuid))
        try:
            if uuid:
                filter_expression = Attr('session_id').eq(uuid)
            else:
                filter_expression = Attr('CPUid').eq(uuid_cpu)
            
            response = self.table.scan(FilterExpression=filter_expression)
            items = response.get('Items', [])
            return items    
        except ClientError as e:
            logger.error(f'Error al obtener los datos:{e.response["Error"]["Message"]}')
            return []
