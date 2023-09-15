import pytest

from experiments.folders.base import BaseTest


@pytest.fixture()
def animal():
    return "file"


class TestAnimal(BaseTest):
    @pytest.fixture()
    def animal(self):
        return "class"

    def test_animal(self, animal):
        assert animal == "class"
