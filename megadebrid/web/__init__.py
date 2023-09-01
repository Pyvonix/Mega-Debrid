import os

from flask import Flask


def create_app(test_config=None):
    """
    Define Flask app for Mega-Web.
    """

    # create and configure the app
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # register blueprints
    from megadebrid.web.views import megaweb

    app.register_blueprint(megaweb)

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app
