
GameObjectTypes=[
    "Resource",
    "Wood",
    "Food",
    "Iron",

    "Unit",
    "Worker",
]

class GameObject:

    def __init__(self, *args, **kwargs):
        for type_ in GameObjectTypes:
            
            setattr(self,
                    'is'+type_,
                    (lambda x : self.__check(x))(type_)
                )
            

    def __check(self, class_str):
        if class_str not in GameObjectTypes:
            return False
        return class_str.lower() in str(type(self)).lower()

