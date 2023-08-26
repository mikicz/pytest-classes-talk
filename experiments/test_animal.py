from enum import Enum

import pytest


class Food(Enum):
    FISH = "fish"
    BONE = "bone"


class Animal:
    def make_sound(self):
        raise NotImplementedError

    def favourite_food(self):
        raise NotImplementedError


class Cat(Animal):
    def make_sound(self):
        return "moew"

    def favourite_food(self):
        return Food.FISH


class Dog(Animal):
    def make_sound(self):
        return "haf"

    def favourite_food(self):
        return Food.BONE


@pytest.mark.parametrize(
    "cls,sound",
    [
        pytest.param(Cat, "moew", id="Cat"),
        pytest.param(Dog, "haf", id="Dog"),
    ],
)
def test_animal_sound(cls, sound):
    assert cls().make_sound() == sound


@pytest.mark.parametrize(
    "cls,food",
    [
        pytest.param(Cat, Food.FISH, id="Cat"),
        pytest.param(Dog, Food.BONE, id="Dog"),
    ],
)
def test_animal_favourite_food(cls, food):
    assert cls().favourite_food() == food


@pytest.mark.parametrize(
    "cls,sound,food",
    [
        pytest.param(Cat, "moew", Food.FISH, id="Cat"),
        pytest.param(Dog, "haf", Food.BONE, id="Dog"),
    ],
)
class TestAnimal:
    def test_sound(self, cls, sound):
        assert cls().make_sound() == sound

    def test_favourite_food(self, cls, food):
        assert cls().favourite_food() == food
