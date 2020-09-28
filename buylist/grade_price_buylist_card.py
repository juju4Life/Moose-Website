

def grade(condition, printing, price):
    grade_value = {
        "Normal": {
            "clean": 1,
            "played": .70,
            "heavily_played": .50,
        },
        "Foil": {
            "clean": 1,
            "played": .60,
            "heavily_played": .30,
        }
    }

    return round(price * grade_value[printing][condition], 2)

