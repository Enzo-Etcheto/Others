import json
import botocore
import boto3

class UADER_IS2_listCorporateData:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('CorporateData')
    def listCorporateData(self, id):
            """Este método recupera todos los elementos de una tabla de DynamoDB y los devuelve como una lista. 
            Si se produce un error del cliente durante la operación, detecta la excepción y devuelve un objeto 
            JSON con un mensaje de error."""
            try:
                response = self.table.scan()
                return response.get('Items', [])
            except botocore.exceptions.ClientError as e:
                return json.dumps({"error": str(e)})

def main():
    site_id = "UADER-FCyT-IS2"
    list_corporate = UADER_IS2_listCorporateData()
    log_corporate = list_corporate.listCorporateData(site_id)
    print(log_corporate)

if __name__ == "__main__":
    main()