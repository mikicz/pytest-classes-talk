import pytest

class BaseTest:
    @pytest.fixture
    def animal(self):
        return "base"
