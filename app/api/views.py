from . import api
from flask import request
from .. import session
from ..models import Currency, Performance, Country
from sqlalchemy import text, func
from .. import engine
from datetime import date
import json, re
from datetime import datetime

@api.route("/")
def home():
    return json.dumps("Welcome to Pana's Currency Converter!")

def countStrings(s):
    
    length = 0
    for i in s:
        if re.search('[a-zA-Z]', i):
            length += 1
    
    return length

def validateISO(s):
    if countStrings(s) == 3 and len(s) == 3:
        return True
    return False

def validateCountryName(c):
    if countStrings(c) + c.count(" ") == len(c):
        return True
    
    return False

def validateDate(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except:
        return False

    return True

@api.route("/get_price", methods=["POST", "GET"])
def getPrice():
    iso = request.args.get('iso')

    if iso == None:
        return json.dumps("Invalid arguments!")
    
    if not validateISO(iso):
        return json.dumps("Invalid input for ISO, can only contain three letters.")
    
    currency = session.query(Currency).filter(Currency.iso == iso.upper()).first()

    if not currency:
        return json.dumps("Currency not found...")
    
    return json.dumps(currency.valuation)

@api.route("/get_evaluation", methods=["POST", "GET"])
def get_evaluation():
    iso_1 = request.args.get("iso1")
    iso_2 = request.args.get("iso2")

    if iso_1 == None or iso_2 == None:
        return json.dumps("Invalid arguments!")
    
    if not validateISO(iso_1):
        return json.dumps("Invalid input for the first ISO, can only contain three letters.")
    
    if not validateISO(iso_2):
        return json.dumps("Invalid input for the second ISO, can only contain three letters.")
    
    currency_1 = session.query(Currency).filter(Currency.iso == iso_1.upper()).first()
    currency_2 = session.query(Currency).filter(Currency.iso == iso_2.upper()).first()

    if not currency_1:
        return json.dumps("First currency not found...")
    
    if not currency_2:
        return json.dumps("Second currency not found...")
    
    difference = abs(currency_1.valuation - currency_2.valuation)
    highest = currency_2
    lowest = currency_1

    if currency_1.valuation < currency_2.valuation:
        highest = currency_1
        lowest = currency_2
    
    return json.dumps({
        "highest" : {
            "name:" : highest.name,
            "value" : highest.valuation 
        },
        "lowest" : {
            "name:" : lowest.name,
            "value" : lowest.valuation 
        },
        "difference": difference
    })

@api.route("/get_performance_report", methods=["POST", "GET"])
def get_performance_report():
    iso = request.args.get("iso")
    country_name = request.args.get("country")
    d1 = request.args.get("start_date")
    d2 = request.args.get("end_date")

    if iso == None or country_name == None or d1 == None or d2 == None:
        return json.dumps("Invalid arguments!")
    
    if not validateCountryName(country_name):
        return json.dumps("Invalid input for country, can only contain letters.")
    
    if not validateISO(iso):
        return json.dumps("Invalid input for ISO, can only contain three letters.")
    
    d1 = [int(i) for i in d1.split("-")]
    d2 = [int(i) for i in d2.split("-")]

    country = session.query(Country).filter(func.lower(Country.name) == country_name.lower()).first()

    if not country:
        return json.dumps("Country not found...")
    
    currency = session.query(Currency).filter(func.lower(Currency.iso) == iso.upper()).first()

    if not currency:
        return json.dumps("Currency not found...")
    
    currencies = session.query(Performance).filter(Performance.currency_id == currency.id, Performance.country_id == country.id, Performance.date >= date(d1[0], d1[1], d1[2]), Performance.date <= date(d2[0], d2[1], d2[2])).order_by(Performance.date.asc()).all()
    
    if not currencies:
        return json.dumps("No records found...")
    
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

@api.route("/get_best_performer", methods=["POST", "GET"])
def get_best_performer():
    specifier = request.args.get("type")
    d = request.args.get("date")

    if d == None or specifier == None:
        return json.dumps("Invalid arguments!")
    
    if not validateDate(d):
        return json.dumps("Invalid input for date, should be YYYY-MM-DD")
    
    d = [int(i) for i in d.split("-")]
    stat = None

    if specifier.lower() == "day":
        stat = session.query(Performance).filter(Performance.date == date(d[0], d[1], d[2])).order_by(Performance.valuation.asc()).first()
    
    if specifier.lower() == "month":
        if d[1] == 12:
            stat = session.query(Performance).filter(Performance.date >= date(d[0], 12, 1), Performance.date < date(d[0], 12, 31)).order_by(Performance.valuation.asc()).first()
        else:
            stat = session.query(Performance).filter(Performance.date >= date(d[0], d[1], 1), Performance.date < date(d[0], d[1] + 1, 1)).order_by(Performance.valuation.asc()).first()
    
    if specifier.lower() == "year":
        stat = session.query(Performance).filter(Performance.date >= date(d[0], 1, 1), Performance.date <= date(d[0], 12, 31)).order_by(Performance.valuation.asc()).first()

    if not stat:
        return json.dumps("No entries for date specified.")
    
    return json.dumps({
        "name" : stat.currency.name,
        "iso": stat.currency.iso,
        "value": stat.valuation,
        "country": stat.country.name
    })
    