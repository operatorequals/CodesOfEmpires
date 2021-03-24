

class Team:

    def __init__(self):
        self.__capacity={
            "food" : 0,
            "wood" : 0,
            "iron" : 0
        }

    def _stockpile(self, value, type_):
        print("Stockpiling",self.__capacity[type_] )
        self.__capacity[type_] += value

Gaia = Team()

