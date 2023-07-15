class ZyxelSessionContext(object):
    def __init__(self):

        self.sessionkey: str = None

        self.encrypted_payloads: bool = None
        self.aes_key = None
        self.public_key = None
