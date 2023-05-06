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

@api.route("/get_evaluation", methods=["POST", "GET"])
def get_evaluation():
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

@api.route("/get_performance_report", methods=["POST", "GET"])
def get_performance_report():
    name = request.args.get("name")
    country = request.args.get("country")
    d1 = request.args.get("start_date").split("-")
    d2 = request.args.get("end_date").split("-")

    currencies = session.query(Performance).filter(func.lower(Performance.name) == str(name).lower(), func.lower(Performance.country) == str(country).lower(), Performance.date >= date(int(d1[0]), int(d1[1]), int(d1[2])), Performance.date <= date(int(d2[0]), int(d2[1]), int(d2[2]))).order_by(Performance.date.asc()).all()
    max = len(currencies)
    deviation = 0
    i = 0

    while i < max:
        nc = i + 1
        if nc < max:
            print(i)
            deviation += currencies[nc].valuation - currencies[i].valuation
        i += 1
    
    return json.dumps({
        "deviation": deviation
    })