from typing import Optional


class NetworkError(Exception):
    def __init__(self, message: Optional[str] = None, body_json: Optional[dict] = None):
        super(NetworkError, self).__init__(message, body_json)
        self.message = message
        self.body_json = body_json
