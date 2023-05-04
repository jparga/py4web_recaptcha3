# Recaptcha V3 for py4web

import requests
from yatl.helpers import DIV, XML, SCRIPT, INPUT
from py4web import request

# Change the settings import with the proper app name
from apps._scaffold import settings

VERIFY_SERVER = "https://www.google.com/recaptcha/api/siteverify"


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

    def __init__(self, token: str = None, score: float = 0.5, action="generic"):
        """
        Initializes the Recaptcha3 class with the public and secret key, token and score
        """
        self.public_key = settings.RECAPTCHA_SITE_KEY
        self.secret_key = settings.RECAPTCHA_SECRET_KEY
        self.token = token
        self.score = score
        self.action = action
        self.response = None
        self.json = None

    def captcha_verify(self) -> dict:
        """
        Verifies the reCAPTCHA token and returns the result and message.
        """
        if not self.token:
            return {"result": False, "message": "Token is missing"}
        url = f"https://www.google.com/recaptcha/api/siteverify?secret={self.secret_key}&response={self.token}&action={self.action}"
        self.response = requests.post(url)
        self.json = self.response.json()
        if self.json["success"] and self.json["score"] > self.score:
            return {"result": True, "message": "You are a human. Aren't you?"}
        else:
            return {
                "result": False,
                "message": "May be you are a bot. If you are human, please try again. "
                + str(self.json["error-codes"]),
            }


class ReCaptchaV3Field:
    def __init__(self, name, action="generic", min_score=0.5):
        """
        Initializes the class with the required fields for reCAPTCHA v3.
        :param name: The name of the reCAPTCHA field.
        :param action: The action that the reCAPTCHA is used for.
        :param min_score: The minimum score required for the reCAPTCHA to be considered valid.
        :param on_captcha_score_low: A callback function to be executed when the reCAPTCHA score is too low.
        """
        self.name = name
        self.action = action
        self.min_score = min_score
        self.site_key = settings.RECAPTCHA_SITE_KEY
        self.secret_key = settings.RECAPTCHA_SECRET_KEY
        self.type = "captcha"
        self.readable = True
        self.writable = True
        self.label = ""
        self.comment = None

    def validate(self, my_token):
        """
        Validates the reCAPTCHA response by sending a request to the Google reCAPTCHA server.
        :param value: The reCAPTCHA response token.
        :param record_id: The id of the record that the reCAPTCHA is associated with.
        :return: A tuple of (validation status, error message)
        """
        my_token = request.POST.get("g-recaptcha-response")

        if not my_token:
            return False, "Missing reCAPTCHA response"
        res = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data=dict(secret=self.secret_key, response=my_token, action=self.action),
        )
        if res.status_code == 200:
            challenge_response = res.json()
            if challenge_response["success"] == True:
                if self.min_score <= challenge_response["score"]:
                    return True, None
                else:
                    if self.on_captcha_score_low:
                        self.on_captcha_score_low(challenge_response["score"])
                    return False, "reCAPTCHA score too low"
        return False, "reCAPTCHA not valid"

    def widget(self, table, my_token):
        """
        Renders the reCAPTCHA widget and the hidden input field.
        :param table: The table that the reCAPTCHA is associated with.
        :param value: The current value of the reCAPTCHA field.
        :return: A DIV element containing the reCAPTCHA widget and the hidden input field.
        """
        return DIV(self.xml())

    def xml(self):
        return XML(
            "<input type='hidden', id='recaptchav3_{name}' name='{name}'>\
                    <script src='https://www.google.com/recaptcha/api.js?render={site_key}'></script>\
                    <script>\
                        grecaptcha.ready(function() {{\
                            grecaptcha.execute('{site_key}', {{action: '{action}'}}).then(function(token) {{\
                                document.getElementById('recaptchav3_{name}').value = token;\
                            }});\
                        }});\
                    </script>".format(
                **dict(name=self.name, action=self.action, site_key=self.site_key)
            )
        )


class RecaptchaWidget:
    def __init__(self, table, value):
        self.table = table
        self.value = value

    def render(self):
        script = """
        function save2form(token){
            document.getElementById("auth_user_recaptcha").value = token;
        }
        """
        for f in self.table:
            if f.name == "recaptcha":
                ret = DIV(
                    SCRIPT(script, _type="text/javascript"),
                    SCRIPT(
                        "",
                        **{
                            "_src": "https://www.google.com/recaptcha/api.js",
                            "_async": "true",
                            "_defer": "true",
                        },
                    ),
                    DIV(
                        **{
                            "_class": "g-recaptcha",
                            "_data-sitekey": settings.RECAPTCHA_SITE_KEY,
                            "_data-callback": "save2form",
                        },
                    ),
                    INPUT(
                        **{
                            "_type": "hidden",
                            "_id": "auth_user_recaptcha",
                            "_name": "recaptcha",
                        },
                    ),
                )
            return ret
