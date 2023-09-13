from enum import Enum


class Food(Enum):
    FISH = "fish"
    BONE = "bone"


class Breeds(Enum):
    LABRADOR = "labrador"


class Tricks(Enum):
    SHAKE_PAW = "paw"


class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        raise NotImplementedError

    def favourite_food(self):
        raise NotImplementedError

    def can_do_tricks(self):
        return False


class Cat(Animal):
    def make_sound(self):
        return "mňau"

    def favourite_food(self):
        return Food.FISH


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
        self.tricks = []

    def make_sound(self):
        return "haf"

    def favourite_food(self):
        return Food.BONE

    def teach_trick(self, trick):
        self.tricks.append(trick)

    def can_do_tricks(self):
        return bool(self.tricks)

    def zoom_around(self):
        return "zoom zoom"

