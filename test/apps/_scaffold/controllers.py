"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL, Field
from yatl.helpers import A, INPUT, DIV
from .common import (
    db,
    session,
    T,
    cache,
    auth,
    logger,
    authenticated,
    unauthenticated,
    flash,
)
from py4web.utils.form import Form
from pydal.validators import IS_NOT_EMPTY

from apps._scaffold import settings
from .recaptcha3 import Recaptcha3


@action("index", method=["GET", "POST"])
@action.uses("index.html", auth, T)
def index():
    message = "Waiting..."
    captcha_site_key = settings.GOOGLE_RECAPTCHA_SITE_KEY
    form = Form(
        [
            Field("product_name"),
        ]
    )

    if form.accepted:
        # Get the token from form
        my_token = request.POST.get("g-recaptcha-response")

        # Get recaptcha response
        captcha = Recaptcha3(token=my_token, score=0.6)

        # Get the verification result
        verificacion = captcha.captcha_verify()

        # Make up your decision
        if verificacion["result"] == True:
            print("Looks like a human")
        else:
            print("Looks like a bot")

        message = verificacion["message"]
    if form.errors:
        # display message error
        message = "Form errors"
    return dict(form=form, message=message, captcha_site_key=captcha_site_key)
