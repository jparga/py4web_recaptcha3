# Recaptcha V3 for py4web

import requests

# Change the settings import with the proper app route
# The Google recaptcha keys coul also be imported from environmen

from .test.apps._scaffold import settings


class Recaptcha3:
    """
    This class allows you to verify reCAPTCHA v3 tokens.

    Attributes:
    public_key (str): The site key provided by Google reCAPTCHA.
    response (requests.Response): The response from the reCAPTCHA server.
    json (dict): The JSON data of the response from the reCAPTCHA server.

    Methods:
    captcha_verify(): Verifies the reCAPTCHA token and returns the result and message.
    """

    def __init__(self, token: str = None, score: float = 0.5):
        """
        Initializes the Recaptcha3 class with the public and secret key, token and score
        """
        self.public_key = settings.GOOGLE_RECAPTCHA_SITE_KEY
        self.secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        self.token = token
        self.score = score
        self.response = None
        self.json = None

    def captcha_verify(self) -> dict:
        """
        Verifies the reCAPTCHA token and returns the result and message.
        """
        if not self.token:
            return {"result": False, "message": "Token is missing"}
        url = f"https://www.google.com/recaptcha/api/siteverify?secret={self.secret_key}&response={self.token}"
        self.response = requests.post(url)
        self.json = self.response.json()
        if self.json["success"] and self.json["score"] > self.score:
            return {"result": True, "message": "You are a human. Aren't you?"}
        else:
            return {
                "result": False,
                "message": "May be you are a bot. If you are human, please reload and try again. "
                + str(self.json["error-codes"]),
            }
