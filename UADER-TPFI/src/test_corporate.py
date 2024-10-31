import unittest
import uuid
import os
from Components.CorporateData import CorporateData
from Components.CorporateLog import CorporateLog

class TestCorporateComponents(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Generación de instancias Singleton para pruebas
        cls.corporate_data = CorporateData.getInstance()
        cls.corporate_log = CorporateLog.getInstance()
        cls.session_id = str(uuid.uuid4())  # ID único de sesión para cada prueba
        cls.uuid_cpu = uuid.getnode()  # Identificador único de CPU
        cls.site_id = "UADER-FCyT-IS2"  # ID de sede para pruebas

    #1- test_singleton_instance: Verifica que las instancias de CorporateData y CorporateLog implementen correctamente el patrón Singleton.
    def test_singleton_instance(self):
        """Verifica que CorporateData y CorporateLog implementan Singleton correctamente."""
        corporate_data2 = CorporateData.getInstance()
        corporate_log2 = CorporateLog.getInstance()
        self.assertIs(self.corporate_data, corporate_data2, "CorporateData no es Singleton")
        self.assertIs(self.corporate_log, corporate_log2, "CorporateLog no es Singleton")

    #2- test_getData: Prueba que getData devuelva la información esperada de la sede y contenga claves como sede y domicilio.
    def test_getData(self):
        """Prueba el método getData de CorporateData para obtener datos de la sede."""
        result = self.corporate_data.getData(self.session_id, self.uuid_cpu, self.site_id)
        self.assertIn("sede", result, "No se encontró la clave 'sede' en la respuesta")
        self.assertIn("domicilio", result, "No se encontró la clave 'domicilio' en la respuesta")

    #3- test_getCUIT: Prueba que getCUIT devuelva el CUIT y contenga las claves CUIT y sede.
    def test_getCUIT(self):
        """Prueba el método getCUIT de CorporateData para obtener el CUIT de la sede."""
        cuit_data = self.corporate_data.getCUIT(self.session_id, self.uuid_cpu, self.site_id)
        self.assertIn("CUIT", cuit_data, "No se encontró el CUIT en la respuesta")
        self.assertIn("sede", cuit_data, "No se encontró la clave 'sede' en la respuesta")

    #4- test_getSeqID: Verifica que getSeqID retorne el ID de secuencia (idSeq).
    def test_getSeqID(self):
        """Prueba el método getSeqID de CorporateData para obtener el identificador de secuencia."""
        seq_id = self.corporate_data.getSeqID(self.session_id, self.uuid_cpu, self.site_id)
        self.assertIn("idSeq", seq_id, "No se encontró 'idSeq' en la respuesta")

    #5- test_post_log: Prueba que post de CorporateLog se ejecute sin errores al registrar una operación.
    def test_post_log(self):
        """Prueba el método post de CorporateLog para registrar una operación en el log."""
        self.corporate_log.post(self.session_id, "getData")
        # No se espera un retorno, solo confirmamos que el método se ejecuta sin errores

    #6- test_list_log: Prueba que list en CorporateLog devuelva una lista de registros, y que cada entrada de log contenga una clave method.
    def test_list_log(self):
        """Prueba el método list de CorporateLog para consultar entradas de log por CPU y sesión."""
        log_entries = self.corporate_log.list(self.uuid_cpu, self.session_id)
        self.assertIsInstance(log_entries, list, "La respuesta de log_entries no es una lista")
        if log_entries:
            self.assertIn("method", log_entries[0], "No se encontró la clave 'method' en la entrada del log")

    #7- test_listCorporateData: Prueba que listCorporateData retorne una lista con todos los registros de CorporateData.
    def test_listCorporateData(self):
        """Prueba el método listCorporateData para obtener todos los registros de la tabla CorporateData."""
        all_data = self.corporate_data.listCorporateData(self.site_id)
        self.assertIsInstance(all_data, list, "La respuesta de listCorporateData no es una lista")

    #8- test_listCorporateLog: Verifica que listCorporateLog en CorporateData retorne una lista.
    def test_listCorporateLog(self):
        """Prueba el método listCorporateLog para obtener todos los registros de la tabla CorporateLog."""
        log_data = self.corporate_data.listCorporateLog(self.uuid_cpu)
        self.assertIsInstance(log_data, list, "La respuesta de listCorporateLog no es una lista")

    # Pruebas adicionales
    #9- test_getData_invalid_id: Verifica que getData retorne un error para un ID inexistente.
    def test_getData_invalid_id(self):
        """Prueba que getData retorne un error para un ID inexistente."""
        invalid_id = "INVALID_ID"
        result = self.corporate_data.getData(self.session_id, self.uuid_cpu, invalid_id)
        self.assertIn("error", result, "No se encontró 'error' en la respuesta para ID inválido")

    #10- test_getCUIT_invalid_id: Verifica que getCUIT retorne un error para un ID inexistente.
    def test_getCUIT_invalid_id(self):
        """Prueba que getCUIT retorne un error para un ID inexistente."""
        invalid_id = "INVALID_ID"
        cuit_data = self.corporate_data.getCUIT(self.session_id, self.uuid_cpu, invalid_id)
        self.assertIn("error", cuit_data, "No se encontró 'error' en la respuesta para ID inválido")

    #11- test_getSeqID_invalid_id: Verifica que getSeqID retorne un error para un ID inexistente.
    def test_getSeqID_invalid_id(self):
        """Prueba que getSeqID retorne un error para un ID inexistente."""
        invalid_id = "INVALID_ID"
        seq_id = self.corporate_data.getSeqID(self.session_id, self.uuid_cpu, invalid_id)
        self.assertIn("error", seq_id, "No se encontró 'error' en la respuesta para ID inválido")

    #12- test_dynamodb_connection_error: Simula un error de conexión para verificar el manejo de errores.
    def test_dynamodb_connection_error(self):
        """Prueba que los métodos manejen un error de conexión de DynamoDB."""
        original_table = self.corporate_data.table
        try:
            # Configura una tabla de prueba inexistente para simular un fallo de conexión
            self.corporate_data.table = self.corporate_data.dynamodb.Table('NonExistentTable')
            result = self.corporate_data.getData(self.session_id, self.uuid_cpu, self.site_id)
            self.assertIn("error", result, "No se encontró 'error' al simular un error de conexión")
        finally:
            # Restaura la tabla original para evitar efectos en otras pruebas
            self.corporate_data.table = original_table

    #13- test_log_post_entry: Verifica que post en CorporateLog registre una entrada con los datos correctos.
    def test_log_post_entry(self):
        """Prueba que post en CorporateLog registre una entrada con los datos correctos."""
        self.corporate_log.post(self.session_id, "testMethod")
        log_entries = self.corporate_log.list(self.uuid_cpu, self.session_id)
        self.assertTrue(any(entry.get('method') == 'testMethod' for entry in log_entries),
                        "No se encontró la entrada de log esperada para 'testMethod'")

    #14- test_getData_missing_arg:
    def test_getData_missing_argument(self):
        """Prueba que getData maneje argumentos faltantes o vacíos."""
        result = self.corporate_data.getData(self.session_id, self.uuid_cpu, "")
        self.assertIn("error", result, "No se encontró 'error' en la respuesta para ID vacío")

if __name__ == "__main__":
    os.system("cls" if os.name == 'nt' else "clear")  # Limpia la consola según el sistema operativo
    unittest.main()
