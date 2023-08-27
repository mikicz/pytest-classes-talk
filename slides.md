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

```python
@pytest.mark.parametrize("cls,sound,food", [
    pytest.param(Cat, "moew", Food.FISH, id="Cat"), 
    pytest.param(Dog, "haf", Food.BONE, id="Dog"),
])
class TestAnimal:
    @pytest.fixture
    def animal(self, cls) -> Animal:
        return cls()
  
    def test_sound(self, animal, sound):
        assert animal.make_sound() == sound
  
    def test_favourite_food(self, animal, food):
        assert animal.favourite_food() == food
```

---

# Fixture availability

- In pytest, fixtures can be shared between files by putting them in `conftest.py`.
- The fixtures in `conftest.py` are available to **all** tests in the folder and all subfolders

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
from .base_cat import BaseCatTest

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

- Function-based tests: **must** rely on folders and conftest.py to organise and share fixtures
  - implicit
  - requires strict discipline
  - big potential for name clashes

<v-click>

- At Xelix, in the primary repository we have
  - 11000 tests in 700 files in 170 folders
  - 4300 unique fixtures

</v-click>

<v-click>

- Class-based tests: **can** rely on inheritance to organise and share fixtures
  - explicit
  - doesn't require as strict of a discipline
  - smaller potential for name clashes

</v-click>

<v-click>

- *Explicit is better than implicit*

</v-click>

---

# Fixtures auto-use

- A fixture which gets used automatically or all tests, without getting explicitly requested 
- If in `conftest.py`, applies to the current folder and subfolders

```python
@pytest.fixture(autouse=True)
def feature_flags(db):
    FeatureFlags.objects.update_or_create(defaults={"use_feature_a": True})
```

<v-click>

### Fixture in class

- Applies to current class and all children

```python
   class TestA:
       @pytest.fixture(autouse=True)
       def feature_flags(self, db):
           FeatureFlags.objects.update_or_create(defaults={"use_feature_a": True})
```

</v-click>

--- 

# Fixtures auto-use

- Using auto-used fixtures defined in `conftest.py` 
  - Can lead to slower tests
  - Can lead to unexpected behaviour

<v-clicks>

- In classes, auto-used fixtures are limited to a set of tests
  - Safer to use
  - Again, more explicit

</v-clicks>

--- 

# Fixture scope

- By default, fixtures get created for each test that uses it
- In this example, the fixture `cat` will be created twice

```python
@pytest.fixture
def cat() -> Cat:
    return Cat()


def test_cat_meows(cat):
    assert cat.make_sound() == "meow"

    
def test_cat_likes_fish(cat):
    assert cat.favourite_food() == Food.FISH
```

---

# Fixture scope

- The *scope* of a fixture can be modified to one of: `function`, `class`, `module`, `package` or `session`
- In this example, the fixture `cat` will be created just once

```python
@pytest.fixture(scope="module")
def cat() -> Cat:
    return Cat()


def test_cat_meows(cat):
    assert cat.make_sound() == "meow"


def test_cat_likes_fish(cat):
    assert cat.favourite_food() == Food.FISH
```

--- 

# Fixture scope

- This works in classes as well

```python
class TestCat:
    @pytest.fixture(scope="class")
    def cat(self) -> Cat:
        return Cat()

    def test_cat_meows(self, cat):
        assert cat.make_sound() == "meow"

    def test_cat_likes_fish(self, cat):
        assert cat.favourite_food() == Food.FISH
```

--- 

# Fixture scope

<v-clicks>

- Primary benefit of appropriate scope is speed
- The slower a fixture is and the more tests use it, the bigger the benefit
- Once created, fixture remains active until all tests in scope finish
  - Can lead to unexpected behaviour, if the fixture has a side-effect (like DB insert)

</v-clicks>

---

# Fixture scope

```python
@pytest.fixture
def cat():
    return Cat.objects.create()  # insert into DB


def test_get_cat(cat, api_client):
    response = api_client.get("/cat/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == cat.id

    
def test_create_cat(api_client):
    response = api_client.post("/cat/", {"name": "Micka"})
    assert response.status_code == 201
    assert Cat.objects.get().name == "Micka"
```

---

# Fixture scope

```python {1,16-17}
@pytest.fixture(scope="module")
def cat():
    return Cat.objects.create()  # insert into DB


def test_get_cat(cat, api_client):
    response = api_client.get("/cat/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == cat.id


def test_create_cat(api_client):
    response = api_client.post("/cat/", {"name": "Micka"})
    assert response.status_code == 201
    # this will no longer work, becaue `cat` fixture scope is still active
    assert Cat.objects.get().name == "Micka"
```

---

# Fixture scope

- Primary benefit of appropriate scope is speed
- The slower a fixture is and the more tests use it, the bigger the benefit
- Once created, fixture remains active until all tests in scope finish
  - Can lead to unexpected behaviour, if the fixture has a side-effect (like DB insert)
  - Especiall problematic with `autouse=True`

<v-clicks>

- Using classes enables using `class`-scoped fixtures, where tests in scope are limited
- In combination with `autouse=True` classes enhance posibilities of setup for a group of tests 

</v-clicks>

