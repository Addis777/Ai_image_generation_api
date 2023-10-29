class APIKeyManager:
    def __init__(self, api_keys):
        self.api_keys = api_keys

    def validate_key(self, key):
        return key in self.api_keys


