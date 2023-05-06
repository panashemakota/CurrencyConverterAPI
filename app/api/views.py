from . import api
from flask import request
from .. import session
from ..models import Currency, Performance
from sqlalchemy import text, func
from .. import engine
from datetime import date
import json

@api.route("/")
def home():
    return "<p>Welcome to Pana's Currency Converter!</p>"

@api.route("/get_price", methods=["POST", "GET"])
def getPrice():
    name = request.args.get('name')
    country = request.args.get('country')
    
    currency = session.query(Currency).filter(func.lower(Currency.name) == str(name).lower(), func.lower(Currency.country) == str(country).lower()).first()

    return json.dumps(currency.valuation)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT valuation FROM currencies WHERE name='" + name + "' AND country='" + country + "'"))
        results = [item[0] for item in result]
        #currency = Currency(results[0][1], results[0][2], results[0][3])

        return json.dumps(results)
        return json.dumps({
            "value": currency.valuation
        })
    return "Database connection failed!"

@api.route("/compare", methods=["POST", "GET"])
def compare():
    name1 = request.args.get("name1")
    country1 = request.args.get("country1")
    name2 = request.args.get("name2")
    country2 = request.args.get("country2")

    currency1 = session.query(Currency).filter(func.lower(Currency.name) == str(name1).lower(), func.lower(Currency.country) == str(country1).lower()).first()
    current2 = session.query(Currency).filter(func.lower(Currency.name) == str(name2).lower(), func.lower(Currency.country) == str(country2).lower()).first()

    difference = abs(currency1.valuation - current2.valuation)

    highest = current2.name
    lowest = currency1.name
    if currency1.valuation < current2.valuation:
        highest = currency1.name
        lowest = current2.name
    
    return json.dumps({
        "difference": difference,
        "highest_value_currency": highest,
        "lowest_value_currency": lowest
    })

@api.route("/get_report", methods=["POST", "GET"])
def get_report():
    name = request.args.get("name")
    country = request.args.get("country")
    start_date = request.args.get("start_date").split("-")
    end_date = request.args.get("end_date").split("-")

    currencies = session.query(Performance).filter(func.lower(Performance.name) == str(name).lower(), func.lower(Performance.country) == str(country).lower(), Performance.date > date(int(start_date[0]), int(start_date[1]), int(start_date[2]))).all()
    items = [[i.valuation, i.date] for i in currencies]

    highest = 0

    for item in items:
        if item[0] > highest:
            highest = item[0]

    lowest = highest

    for item in items:
        if item[0] < lowest:
            lowest = item[0]

    result = highest - lowest

    if result < 0:
        return "Apprciated!"
    else:
        return "Depreciated by " + str(abs(result))

    return json.dumps(items, default=str)