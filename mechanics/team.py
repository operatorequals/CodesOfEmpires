

class Team:

    def __init__(self):
        self.__capacity={
            "food" : 0,
            "wood" : 0,
            "iron" : 0
        }

    def _stockpile(value, type):
        self.__capacity[type] += value

Gaia = Team()

