from Components.Log import Log

class CorporateLog:
    _instance = None

    @staticmethod
    def getInstance():
        if CorporateLog._instance is None:
            CorporateLog._instance = CorporateLog()
        return CorporateLog._instance
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.log = Log()

    def post(self, uuid_session, accion):
        self.log.post(uuid_session, accion)

    def list(self, uuid_cpu, uuid=None):
        return self.log.list(uuid_cpu, uuid)