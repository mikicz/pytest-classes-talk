from .animal import *
from .base import BaseAnimalTest
import pytest



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
