# Recaptcha3

A python class that allows you to verify reCAPTCHA v3 tokens.

A test with py4web \_scaffold app.

Documentation about reCaptcha: https://developers.google.com/recaptcha/docs/v3

## Example

```python3

from recaptcha3 import Recaptcha3

recaptcha = Recaptcha3(token="your_token", score=0.5)
recaptcha.secret_key = "your_secret_key"
recaptcha.public_key = "your_public_key"
result = recaptcha.captcha_verify()
print(result)
```

The example above will output:

`{'result': True, 'message': 'You are a human. Aren't you?'}`

### Test with py4web

In the test folder there is an example for py4web.

The Google recaptcha keys are imported from the settings.py file

## Note

Make sure you have a valid public and secret key from Google reCAPTCHA and a valid token from the user.

## TODO

Recaptcha in auth forms

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update the tests as appropriate.

This README.md file provides a brief overview of how to install and use the class, and gives an example of how to use it. It also provides a note to remind users to have valid public and secret key from Google reCAPTCHA and a valid token from the user.

You can customize it as you like, you can add more information or examples as you need.
Please let me know if you have any other questions.
