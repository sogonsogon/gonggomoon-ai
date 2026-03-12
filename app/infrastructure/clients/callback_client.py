import json
from typing import Any
from urllib import request

from app.application.ports.ports import CallbackPort


class HttpCallbackClient(CallbackPort):
    def send(self, callback_url: str, body: dict[str, Any]) -> None:
        print(f"log : starting to send callback to {callback_url} with body: {body}")

        payload = json.dumps(body).encode("utf-8")
        req = request.Request(
            callback_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=5):
            return
