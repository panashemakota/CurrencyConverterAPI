import os, json
from flask import Flask
from config import app_config
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine("mysql+pymysql://root:1234@localhost/ccapi_db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
db_url = os.environ.get('DATABASE_URL')


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../config.py')

    from app import models
    from .api import api as api_blueprint
    from .models import Currency
    app.register_blueprint(api_blueprint)

    @app.cli.command("create_tables")
    @with_appcontext
    def create_tables():
        Base.metadata.create_all(engine)
        return
    
    app.cli.add_command(create_tables)
    
    @app.cli.command("drop_tables")
    @with_appcontext
    def drop_tables():
        Base.metadata.drop_all(engine)
        return
    
    app.cli.add_command(drop_tables)
    
    @app.cli.command("insert_data")
    @with_appcontext
    def insert_data():
        c1 = Currency(name="Kwacha", country="Zambia", valuation=29)
        c2 = Currency(name="USD", country="United States of America", valuation=1)
        c3 = Currency(name="Bond", country="Zimbabwe", valuation=1400)
        c3 = Currency(name="Australian Dollar", country="Australia", valuation=1400)

        session.add_all([c1,c2,c3])
        session.commit()
        return
    
    app.cli.add_command(insert_data)

    @app.errorhandler(403)
    def forbidden(error):
        return json.dumps("Access denied!"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return json.dumps("URL not found."), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return json.dumps("Internal server error..."), 500


    return app

def create_db():
    Base.metadata.create_all(engine)
    return