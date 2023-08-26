---
footer: 'PyCon CZ, Xth of September 2023'
style: |
    section.intro h1 {
        font-size: 60px;
    }
    section.intro h3 {
        font-size: 50px;
        text-align: right;
        padding-right: 55px;
    }
    footer {
        text-align: right;
    }
lineNumbers: true
---

<!-- _class: intro -->

# **Pytest: The Case for Using Classes**
### a talk by Mikuláš Poul

<!--
Example speaker note
-->

---

# About me

- he/him, go by Miki
- Born in the Czech Republic
- Live in London, UK

<v-clicks>

- Have been coding in Python for 10 years
- Have been using Pytest for last X years  # TODO: find
- Staff Engineer at Xelix # TODO: link, logo
- www.mikulaspoul.cz  # TODO: link

</v-clicks>

<!--
Mention all links are on mikulaspoul, plus a blog
-->

---

# Pytest

A beloved testing framework with several massive features

<v-click>

- Minimal test setup
- Simple asserts

```python
def test_cat():
    assert Cat().make_sound() == "meow"
```

</v-click>

<v-click>

- Fixtures - reusable test setup

<!--
First ask who writes tests, who uses pytest, and who uses classes?
-->

```python
@pytest.fixture
def cat() -> Cat:
    return Cat()


def test_cat_meows(cat):
    assert cat.make_sound() == "meow
```

</v-click>

---

# Why care how tests are written?

<v-clicks>

- Writing tests takes up a big part of coding time
- Maintainability of tests equals maintainability of entire codebase
  - Tests usually compose a big part of codebase
  - At Xelix, in the primary repository tests take up ~1/3 of files and ~1/2 lines of code
- At scale
  - Running tests can take a long time
  - TODO: somehow say reusability is important

</v-clicks>

---

# So - classes you say?

```python
class TestCat:
    @pytest.fixture
    def cat(self) -> Cat:
        return Cat()
    
    def test_meows(self, cat):
        assert cat.make_sound() == "meow"
```

---

# Targetting 

By default, you can use the following targetting for running tests

```text
pytest tests/test_cat.py::test_cat_meows
       |     |            \
       |     \             specific test
       \      specific file
        specific folder                   
```

---

# Targetting

With classes, that extends to being able to target a specific class

```text
pytest tests/test_cat.py::TestCat::test_meows
       |     |            |        \
       |     |            \         specific test
       |     \             specific class
       \      specific file
        specific folder                   
```

---

<!-- _lineNumbers: true -->

# Compactness 1 

```python
@pytest.mark.some_mark
def test_cat_meows(cat):
    assert cat.make_sound() == "meow"


@pytest.mark.some_mark
def test_cat_likes_fish(cat):
    assert cat.favourite_food() == Food.FISH
```

<v-click>

Becomes

```python
class TestCat:
    pytestmark = pytest.mark.some_mark
    
    def test_meows(self, cat):
        assert cat.make_sound() == "meow"
    
    def test_likes_fish(self, cat):
        assert cat.favourite_food() == Food.FISH
```

</v-click>

---

# Compactness 2

```python
@pytest.mark.parametrize("cls,sound", [
    pytest.param(Cat, "moew", id="Cat"), 
    pytest.param(Dog, "haf", id="Dog"),
])
def test_animal_sound(cls, sound):
    assert cls().make_sound() == sound


@pytest.mark.parametrize("cls,food", [
    pytest.param(Cat, Food.FISH, id="Cat"), 
    pytest.param(Dog, Food.BONE, id="Dog"),
])
def test_animal_favourite_food(cls, food):
    assert cls().favourite_food() == food
```

---

# Compactness 2

Becomes

TODO: fix this not actually working as an example because the fixture needs to be used in the other test

```python
@pytest.mark.parametrize("cls,sound,food", [
    pytest.param(Cat, "moew", Food.FISH, id="Cat"), 
    pytest.param(Dog, "haf", Food.BONE, id="Dog"),
])
class TestAnimal:
    def test_sound(self, cls, sound):
        assert cls().make_sound() == sound
  
    def test_favourite_food(self, cls, food):
        assert cls().favourite_food() == food
```

---

# Fixture availability

- In pytest, fixtures can be shared between files by putting them in `conftest.py`.
- The fixtures in `conftest.py` are available to *all* tests in the folder and all subfolders

<v-click>

```python
# tests/animals/test_cat.py

def test_cat(cat):
    pass
```

</v-click>

<v-click>

```text {0|5|4|2} {lineNumbers: false}
tests/
  conftest.py    priority 2
  animals/       
    conftest.py  priority 1
    test_cat.py  priority 0
```

</v-click>

---

# Fixture availability

```python
# tests/animals/test_cat.py

class TestCat:
    def test_cat(self, cat):
        pass
```

<v-click>

```text {0|6|5|4|2} {lineNumbers: false}
tests/
  conftest.py    priority 3
  animals/       
    conftest.py  priority 2
    test_cat.py  priority 1
        TestCat  priority 0
```

</v-click>

---

# Class inheritance

```python
# tests/animals/test_cat.py
from .base import BaseCatTest

class TestCat(BaseCatTest):
    def test_cat(self, cat):
        pass
```

<v-click>

```text {0|8|6|7|4|2} {lineNumbers: false}
tests/
  conftest.py        priority 4
  animals/       
    conftest.py      priority 3
    base_cat.py  
        BaseCatTest  priority 1
    test_cat.py      priority 2
        TestCat      priority 0
```

</v-click>

---

# Namespace cleanliness

11000 tests in 700 files in 170 folders, total of 4300 unique fixtures

- Function-based tests: **must** rely on folders and conftest.py to organise and share fixtures
  - implicit
  - requires strict discipline
  - big potential for name clashes

<v-click>

- Class-based tests: **can** rely on inheritance to organise and share fixtures
  - explicit
  - doesn't require as strict of a discipline
  - smaller potential for name clashes

</v-click>
