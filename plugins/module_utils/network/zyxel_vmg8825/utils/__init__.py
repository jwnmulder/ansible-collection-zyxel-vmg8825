class ZyxelSessionContext(object):
    def __init__(self):

        self.sessionkey: str = None

        self.encrypted_payloads = None
        self.client_aes_key = None
        self.router_public_key = None
