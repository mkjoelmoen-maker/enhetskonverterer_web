import requests

API_KEY = "fca_live_VNWmAJG5gsWbOLYgGe9VPzM2UH5VyhqF98QFXiOJ"
BASE_URL = "https://api.freecurrencyapi.com/v1/latest"

def convert_units(value, from_unit, to_unit, category):
    value = float(value)
    
    if category == "Lengde":
        factors = {
            "meter": 1,
            "centimeter": 100,
            "kilometer": 0.001,
            "inch": 39.3701,
            "foot": 3.28084,
            "mile": 0.000621371,
            "yard": 1.09361     # ← ny
        }
    elif category == "Vekt":
        factors = {
            "kilogram": 1,
            "gram": 1000,
            "pund": 2.20462,
            "ounce": 35.274,
            "tonn": 0.001,
            "stone": 0.157473    # ← ny (1 stone ≈ 6.35029 kg)
        }
    elif category == "Volum":
        factors = {
            "liter": 1,
            "milliliter": 1000,
            "gallon": 0.264172,
            "pint": 2.11338,
            "kubikkmeter": 0.001
        }
    elif category == "Tid":
        factors = {
            "sekund": 1,
            "minutt": 1/60,
            "time": 1/3600,
            "dag": 1/86400
        }
    elif category == "Temperatur":
        return convert_temperature(value, from_unit, to_unit)
    else:
        return None
    
    return value * (factors[to_unit] / factors[from_unit])

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            return value * 9/5 + 32
        elif to_unit == "Kelvin":
            return value + 273.15
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            return value - 273.15
        elif to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32

def convert_currency(amount, from_curr, to_curr):
    params = {
        "apikey": API_KEY,
        "base_currency": from_curr,
        "currencies": to_curr
    }
    resp = requests.get(BASE_URL, params=params)
    data = resp.json()

    if "data" not in data or to_curr not in data["data"]:
        raise Exception("Ugyldig valuta valgt eller API-feil")

    rate = data["data"][to_curr]
    return amount * rate

