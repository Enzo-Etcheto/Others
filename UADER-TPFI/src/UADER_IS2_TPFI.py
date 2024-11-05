from Components.CorporateData import CorporateData
from Components.CorporateLog import CorporateLog
import uuid
from datetime import datetime
import json


def main():
    # Generación automática de identificadores y timestamp
    session_id = str(uuid.uuid4())  
    uuid_cpu = uuid.getnode()         
    site_id = "UADER-FCyT-IS2"      
    
    # Instancias Singleton de CorporateData y CorporateLog
    print("Instanciando objetos:")
    corporate_data = CorporateData.getInstance()
    corporate_log = CorporateLog.getInstance()

    # Llamada a getData
    print("Obteniendo datos:")
    data = corporate_data.getData(session_id, uuid_cpu, site_id)
    # Cargar el JSON y luego imprimirlo de manera legible
    try:
        formatted_data = json.loads(data)
        print(json.dumps(formatted_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"Ocurrió un error al decodificar el JSON: {str(e)}")

    # Registrar operación con CorporateLog - método post
    print("\nRegistrando operación en log:")
    corporate_log.post(session_id, "getData")

    # Llamada a getCUIT
    print("\nObteniendo CUIT:")
    cuit_data = corporate_data.getCUIT(session_id, uuid_cpu, site_id)
    try:
        formatted_data = json.loads(cuit_data)
        print(json.dumps(formatted_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"Ocurrió un error al decodificar el JSON: {str(e)}")

    # Registrar operación con CorporateLog - método post
    print("\nRegistrando operación en log:")
    corporate_log.post(session_id, "getCUIT")

    #Llamada a getSeqID
    print("\nObteniendo ID de secuencia:")
    seq_id = corporate_data.getSeqID(session_id, uuid_cpu, site_id)
    try:
        formatted_data = json.loads(seq_id)
        print(json.dumps(formatted_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"Ocurrió un error al decodificar el JSON: {str(e)}")

    # Registrar operación con CorporateLog - método post
    print("\nRegistrando operación en log:")
    corporate_log.post(session_id, "getSeqID")

    # Listar registros con CorporateData
    print("\nListando registros CorporateData:")
    log_entriesCorporateData = corporate_data.listCorporateData(site_id)
    print("Entradas de log:", log_entriesCorporateData)


    # Listar registros con CorporateLog
    print("\nListando registros CorporateLog:")
    log_entriesCorporateLog = corporate_data.listCorporateLog(uuid_cpu)
    print("Entradas de log:", log_entriesCorporateLog)

    # Consultar el log usando CorporateLog - método list
    print("\nConsultando registros en log:")
    log_entriesList = corporate_log.list(uuid_cpu, session_id)
    print("Entradas de log:", log_entriesList)

if __name__ == "__main__":
    main()