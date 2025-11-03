from flask import Flask, render_template, request
from enhetskonverterer import convert_units, convert_temperature, convert_currency

app = Flask(__name__)

# Enheter og kategorier
units = {
    "Lengde": ["meter", "centimeter", "kilometer", "inch", "foot", "mile"],
    "Vekt": ["kilogram", "gram", "pund", "ounce", "tonn"],
    "Volum": ["liter", "milliliter", "gallon", "pint", "kubikkmeter"],
    "Tid": ["sekund", "minutt", "time", "dag"],
    "Temperatur": ["Celsius", "Fahrenheit", "Kelvin"],
    "Valuta": ["USD", "EUR", "GBP", "NOK", "JPY", "AUD"]
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    selected_category = "Lengde"
    from_unit = ""
    to_unit = ""
    value = ""
    
    if request.method == "POST":
        selected_category = request.form["category"]
        from_unit = request.form["from_unit"]
        to_unit = request.form["to_unit"]
        value = request.form["value"]

        try:
            val = float(value)
            if selected_category == "Valuta":
                result_value = convert_currency(val, from_unit, to_unit)
            elif selected_category == "Temperatur":
                result_value = convert_temperature(val, from_unit, to_unit)
            else:
                result_value = convert_units(val, from_unit, to_unit, selected_category)
            
            # Format med komma
            result = f"{result_value:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception as e:
            result = f"⚠️ Feil: {e}"

    return render_template("index.html", units=units, selected_category=selected_category,
                           from_unit=from_unit, to_unit=to_unit, value=value, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
