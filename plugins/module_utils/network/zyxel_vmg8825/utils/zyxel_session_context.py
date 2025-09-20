class ZyxelSessionContext:
    SESSIONKEY_METHOD_QUERY_PARAM = "query_param"
    SESSIONKEY_METHOD_CSRF_TOKEN = "CSRFToken"

    def __init__(self):
        # sessionkey is required for CSRF checks done by the router
        self.sessionkey = None

        # router api capabilities
        self.sessionkey_method = None
        self.encrypted_payloads = None

        # crypto related keys for the current session
        self.client_aes_key = None
        self.router_public_key = None
