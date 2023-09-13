import pytest
from .animal import Animal


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
