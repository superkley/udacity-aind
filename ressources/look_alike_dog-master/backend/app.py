"""App module containing create_app factory function."""
from flask import Flask

from backend import commands
from backend.blueprints import look_alike_dog
from backend.settings import DevConfig, ProdConfig


def create_app(config_object=ProdConfig):
    """
    An application factory method.

    :note: Explanation here: http://flask.pocoo.org/docs/patterns/appfactories

    :param config_object: Configuration object to use.
    :return: flask application object
    """

    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    register_blueprints(app)
    register_errorhandlers(app)
    register_commands(app)

    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(look_alike_dog.views.blueprint)


def register_errorhandlers(app):
    """
    Register error handlers to show custom error pages.
    
    :note: Explanation here: http://flask.pocoo.org/docs/0.12/patterns/errorpages/
    """
    return None


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)


if __name__ == "__main__":
    """Run server for local development"""
    app = create_app(config_object=DevConfig)
    app.run()

