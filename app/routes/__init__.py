from .users import users_bp
from .characters import characters_bp


def register_blueprints(app):
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(characters_bp, url_prefix="/characters")
