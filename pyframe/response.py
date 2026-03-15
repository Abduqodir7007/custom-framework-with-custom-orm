import json
from typing import Any

from webob import Response as WebobResponse


class Response:
    def __init__(self) -> None:
        self.json = None
        self.text = None
        self.content_type = None
        self.body = b""
        self.status_code = 200

    def change_response(self):

        if self.json is not None:
            self.body = json.dumps(self.json).encode()
            self.content_type = "application/json"

        if self.text is not None:
            self.body = self.text
            self.content_type = "text/plain"

    def __call__(self, environ, start_response) -> Any:
        self.change_response()
        response = WebobResponse(
            body=self.body, status=self.status_code, content_type=self.content_type
        )

        return response(environ, start_response)
