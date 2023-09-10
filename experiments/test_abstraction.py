from enum import Enum

import pytest


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


class BaseAnimalTest:
    ANIMAL_SOUND = None
    FAVOURITE_FOOD = None
    CAN_DO_TRICKS = False

    @pytest.fixture(scope="class")
    def animal(self) -> Animal:
        raise NotImplementedError()

    def test_sound(self, animal):
        assert animal.make_sound() == self.ANIMAL_SOUND

    def test_favourite_food(self, animal):
        assert animal.favourite_food() == self.FAVOURITE_FOOD

    def test_can_do_tricks(self, animal):
        assert animal.can_do_tricks() == self.CAN_DO_TRICKS


class TestCat(BaseAnimalTest):
    ANIMAL_SOUND = "mňau"
    FAVOURITE_FOOD = Food.FISH

    @pytest.fixture
    def animal(self) -> Cat:
        return Cat(name="Micka")


class TestDog(BaseAnimalTest):
    ANIMAL_SOUND = "haf"
    FAVOURITE_FOOD = Food.BONE
    CAN_DO_TRICKS = True

    @pytest.fixture
    def animal(self) -> Dog:
        dog = Dog(name="Max", breed=Breeds.LABRADOR)
        dog.teach_trick(Tricks.SHAKE_PAW)
        return dog

    def test_zoomies(self, animal):
        animal.zoom_around()
