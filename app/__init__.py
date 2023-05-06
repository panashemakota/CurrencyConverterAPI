import os, json
from datetime import date
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
    from .models import Currency, Performance
    app.register_blueprint(api_blueprint)

    @app.cli.command("drop_tables")
    @with_appcontext
    def drop_tables():
        Base.metadata.drop_all(engine)
        return
    
    app.cli.add_command(drop_tables)
    
    @app.cli.command("insert_data")
    @with_appcontext
    def insert_data():
        data = [
            Currency(name="Kwacha", iso="ZMW", country="Zambia", valuation=29),
            Currency(name="USD", iso="USD", country="United States of America", valuation=1),
            Currency(name="Bond", iso="ZWD", country="Zimbabwe", valuation=1400),
            Currency(name="Australian Dollar", iso="AUD", country="Australia", valuation=1400),
            Performance(name="Kwacha", iso="ZMW", country="Zambia", valuation=29, date=date(2023, 3, 21)),
            Performance(name="Kwacha", iso="ZMW", country="Zambia", valuation=30, date=date(2023, 2, 21)),
            Performance(name="Kwacha", iso="ZMW", country="Zambia", valuation=22, date=date(2023, 1, 21)),
            Performance(name="Kwacha", iso="ZMW", country="Zambia", valuation=22, date=date(2022, 12, 21)),
            Performance(name="USD", iso="USD", country="United States of America", valuation=1, date=date(2023, 5, 12)),
            Performance(name="USD", iso="USD", country="United States of America", valuation=1.5, date=date(2023, 2, 12)),
            Performance(name="Bond", iso="ZWD", country="Zimbabwe", valuation=1400, date=date(2023, 1, 1)),
            Performance(name="Bond", iso="ZWD", country="Zimbabwe", valuation=1800, date=date(2023, 8, 1)),
            Performance(name="Bond", iso="ZWD", country="Zimbabwe", valuation=800, date=date(2022, 1, 1)),
            Performance(name="Bond", iso="ZWD", country="Zimbabwe", valuation=300, date=date(2022, 5, 1)),
            Performance(name="Bond", iso="ZWD", country="Zimbabwe", valuation=400, date=date(2022, 8, 1)),
            Performance(name="Australian Dollar", iso="AUD", country="Australia", valuation=1400)
        ]

        session.add_all(data)
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