
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    dob1 = datetime.strptime(data["dob1"], "%Y-%m-%d")
    dob2 = datetime.strptime(data["dob2"], "%Y-%m-%d")

    def calculate_life_path(dob):
        digits = [int(d) for d in dob.strftime("%Y%m%d")]
        total = sum(digits)
        while total not in [11, 22, 33] and total > 9:
            total = sum([int(d) for d in str(total)])
        return total

    def calculate_character_number(dob):
        total = sum([int(d) for d in str(dob.day)])
        while total > 9:
            total = sum([int(d) for d in str(total)])
        return total

    def get_day_master_and_strength(dob):
        month = dob.month
        if month in [1, 2]: return "Strong Water"
        elif month in [3, 4]: return "Weak Wood"
        elif month in [5, 6]: return "Strong Fire"
        elif month in [7, 8]: return "Weak Metal"
        elif month in [9, 10]: return "Strong Earth"
        elif month in [11, 12]: return "Weak Fire"
        return "Unknown"

    def get_zodiac(dob):
        zodiacs = ["Monkey", "Rooster", "Dog", "Pig", "Rat", "Ox",
                   "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat"]
        return zodiacs[(dob.year - 1900) % 12]

    result = {
        "P1 Life Path": calculate_life_path(dob1),
        "P2 Life Path": calculate_life_path(dob2),
        "P1 Character": calculate_character_number(dob1),
        "P2 Character": calculate_character_number(dob2),
        "P1 Element": get_day_master_and_strength(dob1),
        "P2 Element": get_day_master_and_strength(dob2),
        "P1 Zodiac": get_zodiac(dob1),
        "P2 Zodiac": get_zodiac(dob2),
        "Life Path": "Green",
        "Character Number": "Green",
        "Zodiac": "Green",
        "Element": "Green"
    }

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
