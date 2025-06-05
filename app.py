from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# ✅ CORS Fix for specific origins (Vercel)
CORS(app, resources={r"/api/*": {"origins": [
    "https://matchmaking-frontend-nine.vercel.app",
    "https://matchmaking-frontend-py0cmfefu-s1d79s-projects.vercel.app"
]}})



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
        day = dob.day
        total = sum([int(d) for d in str(day)])
        while total > 9:
            total = sum([int(d) for d in str(total)])
        return total

    zodiac_map = {
        0: "Monkey", 1: "Rooster", 2: "Dog", 3: "Pig", 4: "Rat", 5: "Ox",
        6: "Tiger", 7: "Rabbit", 8: "Dragon", 9: "Snake", 10: "Horse", 11: "Goat"
    }

    def get_chinese_zodiac(dob):
        return zodiac_map[(dob.year - 1900) % 12]

    def get_day_master_and_strength(dob):
        month = dob.month
        if month in [1, 2]: return "Strong Water"
        elif month in [3, 4]: return "Weak Wood"
        elif month in [5, 6]: return "Strong Fire"
        elif month in [7, 8]: return "Weak Metal"
        elif month in [9, 10]: return "Strong Earth"
        elif month in [11, 12]: return "Weak Fire"
        return "Unknown"

    element_compatibility = {
        "Strong Earth": {"good": ["Wood", "Metal"], "wealth": ["Water"]},
        "Weak Earth": {"good": ["Earth", "Fire"], "wealth": []},
        "Strong Wood": {"good": ["Fire", "Metal"], "wealth": ["Earth"]},
        "Weak Wood": {"good": ["Wood", "Water"], "wealth": []},
        "Strong Fire": {"good": ["Earth", "Water"], "wealth": ["Metal"]},
        "Weak Fire": {"good": ["Fire", "Wood"], "wealth": []},
        "Strong Metal": {"good": ["Fire", "Water"], "wealth": ["Wood"]},
        "Weak Metal": {"good": ["Metal", "Earth"], "wealth": []},
        "Strong Water": {"good": ["Earth", "Wood"], "wealth": ["Fire"]},
        "Weak Water": {"good": ["Water", "Metal"], "wealth": []},
    }

    def evaluate_element_compatibility(dm1, dm2):
        e1 = dm1.split()[-1]
        e2 = dm2.split()[-1]
        if e2 in element_compatibility.get(dm1, {}).get("wealth", []): return "Blue"
        if e2 in element_compatibility.get(dm1, {}).get("good", []): return "Green"
        return "Red"

    lp_compat = {
        1: {"good": [2, 3, 5, 7], "bad": [1, 8]},
        2: {"good": [2, 8, 9], "bad": [4, 7]},
        3: {"good": [2, 5, 7], "bad": [3, 8]},
        4: {"good": [1, 7, 8], "bad": [3, 5]},
        5: {"good": [7], "bad": [4, 8]},
        6: {"good": [1, 2, 9], "bad": [3, 5]},
        7: {"good": [3, 4, 5], "bad": [1, 2, 8]},
        8: {"good": [2, 3, 4], "bad": [1]},
        9: {"good": [2, 3, 6], "bad": [8]},
        11: {"good": [7, 9, 11], "bad": [2]},
        22: {"good": [7, 8], "bad": [5]},
        33: {"good": [1, 2, 9], "bad": []}
    }

    def lp_match(a, b):
        if b in lp_compat.get(a, {}).get("good", []): return "Green"
        if b in lp_compat.get(a, {}).get("bad", []): return "Red"
        return "Neutral"

    friends = [
        ["Rat", "Dragon", "Monkey"], ["Ox", "Snake", "Rooster"],
        ["Tiger", "Horse", "Dog"], ["Rabbit", "Goat", "Pig"]
    ]
    enemies = [("Rat", "Horse"), ("Ox", "Goat"), ("Tiger", "Monkey"),
               ("Rabbit", "Rooster"), ("Dragon", "Dog"), ("Snake", "Pig")]

    def zodiac_match(z1, z2):
        for g in friends:
            if z1 in g and z2 in g: return "Green"
        if (z1, z2) in enemies or (z2, z1) in enemies: return "Red"
        return "Neutral"

    result = {
        "P1 Life Path": calculate_life_path(dob1),
        "P2 Life Path": calculate_life_path(dob2),
        "P1 Character": calculate_character_number(dob1),
        "P2 Character": calculate_character_number(dob2),
        "P1 Zodiac": get_chinese_zodiac(dob1),
        "P2 Zodiac": get_chinese_zodiac(dob2),
        "P1 Element": get_day_master_and_strength(dob1),
        "P2 Element": get_day_master_and_strength(dob2),
    }

    result["Life Path"] = lp_match(result["P1 Life Path"], result["P2 Life Path"])
    result["Character Number"] = lp_match(result["P1 Character"], result["P2 Character"])
    result["Zodiac"] = zodiac_match(result["P1 Zodiac"], result["P2 Zodiac"])
    result["Element"] = evaluate_element_compatibility(result["P1 Element"], result["P2 Element"])

    return jsonify(result)
