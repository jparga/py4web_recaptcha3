import json
import requests
from py4web import request


class Recaptcha3:

    # Estos valores se importarán de settings_private.py en cada aplicación
    GOOGLE_RECAPTCHA_SITE_KEY = " "
    GOOGLE_RECAPTCHA_SECRET_KEY = " "

    API_URI = "https://www.google.com/recaptcha/api.js"
    VERIFY_SERVER = "https://www.google.com/recaptcha/api/siteverify"

    def __init__(
        self,
        request=None,
        public_key="",
        private_key="",
        error_message="invalid",
        label="Verify:",
        options=None,
        comment="",
    ):
        request = request.POST.get("g-recaptcha-response")
        # self.request_vars = request and request.get(vars)
        # self.remote_addr = request.environ['REMOTE_ADDR']
        self.public_key = public_key
        self.private_key = private_key
        self.errors = dict()
        self.error_message = error_message
        self.components = []
        self.attributes = {}
        self.label = label
        self.options = options or {}
        self.comment = comment

    def _validate(self):
        recaptcha_response = request
        data = {"secret": self.private_key, "response": recaptcha_response}
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        result = r.json()
        print(result)
