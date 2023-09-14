---
lineNumbers: true
download: true
theme: dracula
highlighter: shiki
favicon: '/favicon.png'
fonts:
  sans: "Barlow"
---

# **Pytest: The Case for Using Classes**

### a talk by Mikuláš Poul
### September 16, 2023 - PyCon CZ

<!--

This talk
  - will try to showcase using classes in pytest and benefits
  - teach you a bit about pytest

-->

---

# About me

- he/him, go by Miki
- Born in the Czech Republic
- Live in London, UK

<v-clicks>

- Have been coding in Python for 10 years
- Have been using Pytest for last 8 years
- Staff Engineer at [<img src="/xelix.svg" style="display: inline; height: 25px; margin-top: -10px" />](https://xelix.com/)
- [www.mikulaspoul.cz](https://www.mikulaspoul.cz/)

</v-clicks>

<!--
Still a little bit in the imposter syndrome phase of being a staff engineer

Mention all links & relevant details are on mikulaspoul, plus a blog and link to this talk
-->

---

# Pytest

A beloved testing framework with several massive features

<v-clicks>

- Minimal test setup
- Simple asserts

</v-clicks>

<v-click>

```python
def test_cat():
    assert Cat().make_sound() == "mňau"
```

</v-click>


<!--
First ask who writes tests, who uses pytest, and who uses classes?
-->

---

# Pytest

A beloved testing framework with several massive features

- Fixtures - reusable test setup

```python
@pytest.fixture
def cat() -> Cat:
    return Cat()

def test_cat_meows(cat):
    assert cat.make_sound() == "mňau"
```

---

# Why care how tests are written?

<v-clicks>

- Writing tests takes up a big part of coding time
- Maintainability of tests equals maintainability of entire codebase
  - Tests usually compose a big part of codebase
  - At Xelix, in the primary repo tests take up ~1/3 of files and ~1/2 lines of code
- At scale
  - Running tests can take a long time
  - Reusing parts of tests can speed up development 

</v-clicks>

---

# Classes you say?

```python
class TestCat:
    @pytest.fixture
    def cat(self) -> Cat:
        return Cat()
    
    def test_meows(self, cat):
        assert cat.make_sound() == "mňau"
```

<!--
The class needs to be called TestSomething for pytest to pick it up.
-->

---
layout: statement
---

# Benefits of using clases

---
layout: section
---

# Grouping tests

---

# Another way of grouping tests

- Classes can serve to group tests in the same file

<v-clicks>

- Helps with orientiation within code
- You can run just a specific class of tests

</v-clicks>

---

# Targeting

<v-clicks>

```text
pytest                                          # run all tests
```

```text
pytest tests/                                   # run tests in folder
```
```text
pytest tests/test_cat.py                        # run tests in file
```
```text
pytest tests/test_cat.py::test_cat_meows        # run specific test
```
```text
pytest tests/test_cat.py::TestCat               # run test class
```
```text
pytest tests/test_cat.py::TestCat::test_moews   # run specific test in class
```

```text
pytest -k Cat                                   # all tests with Cat in ID
```

</v-clicks>

---
layout: section
---

# More compact tests

---

# Compactness / Repetitiveness 1

```python
@pytest.fixture
def cat() -> Cat:
    return Cat()


@pytest.mark.skip_ci
def test_cat_meows(cat):
    assert cat.make_sound() == "mňau"


@pytest.mark.skip_ci
def test_cat_likes_fish(cat):
    assert cat.favourite_food() == Food.FISH
```


---

# Compactness / Repetitiveness 1

```python
@pytest.mark.skip_ci
class TestCat:
    @pytest.fixture
    def cat(self) -> Cat:
        return Cat()
  
    def test_meows(self, cat):
        assert cat.make_sound() == "mňau"
    
    def test_likes_fish(self, cat):
        assert cat.favourite_food() == Food.FISH
```

<!--

Mention
  - class name
  - pytestmark
  - not needing to repeat test_cat

-->

---

# Compactness / Repetitiveness 2

```python
@pytest.mark.parametrize("cls,sound", [
    pytest.param(Cat, "mňau", id="Cat"), 
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

# Compactness / Repetitiveness 2

```python
@pytest.mark.parametrize("cls,sound,food", [
    pytest.param(Cat, "mňau", Food.FISH, id="Cat"), 
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

# So why do I think classes are better for tests?

- Additional grouping choice 
- Smaller code footprint
- Reduced repetitions

---
layout: section
---

# Explicit fixture availability

---

# Fixture availability

- In pytest, fixtures can be shared between files by putting them in `conftest.py`
- Fixtures in `conftest.py` are available to **all** tests in the folder and all subfolders

---
layout: two-cols
---

::default::

# Fixture availability

<v-click>

```python
# tests/animals/test_cat.py


def test_cat(cat):
    pass

```

</v-click>

<v-click>

```text {0|5|4|2|7|8} {lineNumbers: false}
tests/
  conftest.py           priority 2
  animals/       
    conftest.py         priority 1
    test_cat.py         priority 0

conftest.py             priority 3
```

</v-click>

::right::

# &nbsp;

<v-click>

```python
# tests/animals/test_cat.py

class TestCat:
    def test_cat(self, cat):
        pass
```

</v-click>

<v-click>

```text {0|6|5|4|2|7} {lineNumbers: false}
tests/
  conftest.py           priority 3
  animals/       
    conftest.py         priority 2
    test_cat.py         priority 1
        TestCat         priority 0
conftest.py             priority 4
```

</v-click>

---
layout: two-cols
---

# Class inheritance

```python
# tests/animals/test_cat.py


class TestCat:
    def test_cat(self, cat):
        pass
```

```text {10} {lineNumbers: false}
tests/
  conftest.py           priority 3
  animals/       
    conftest.py         priority 2


    test_cat.py         priority 1
        TestCat         priority 0
conftest.py             priority 4
```

::right::

# &nbsp;

<v-click>

```python
# tests/animals/test_cat.py
from .base_cat import BaseCatTest

class TestCat(BaseCatTest):
    def test_cat(self, cat):
        pass
```

</v-click>


<v-click>

```text {0|8|6|7|4|2|9} {lineNumbers: false}
tests/
  conftest.py           priority 4
  animals/       
    conftest.py         priority 3
    base_cat.py  
        BaseCatTest     priority 1
    test_cat.py         priority 2
        TestCat         priority 0
conftest.py             priority 5
```

</v-click>

---

# Namespace cleanliness

- Function-based tests: **must** rely on folders and conftest.py to share fixtures
  - implicit
  - big potential for name clashes

<v-click>

- Class-based tests: **can** rely on inheritance to organise and share fixtures
  - explicit
  - smaller potential for name clashes

</v-click>

<v-click>

- At Xelix, in the primary repository we have
  - 11000 tests in 700 files in 170 folders
  - 4300 unique fixtures

</v-click>

<v-click>

- *Explicit is better than implicit*

</v-click>

<!--
Function-based tests require a lot of discipline to share fixtures well.
With classes, as long as you don't just put all your fixtures in the same base classes, less discipline is needed.
-->

---

# So why do I think classes are better for tests?

- Additional grouping choice 
- Smaller code footprint
- Reduced repetitions
- Explicit fixture availability
- Cleaner fixture namespace

---
layout: section
---

# Safer auto-used fixtures

---

# Auto-used fixtures

- A fixture which gets used on all tests, without getting explicitly requested 
- If in `conftest.py`, applies to the current folder and subfolders

```python
@pytest.fixture(autouse=True)
def feature_flags(db):
    FeatureFlags.objects.update_or_create(defaults={"use_feature_a": True})
```

---

# Auto-used fixtures in class

- Applies to current class instance

```python
class TestA:
    @pytest.fixture(autouse=True)
    def feature_flags(self, db):
        FeatureFlags.objects.update_or_create(defaults={"use_feature_a": True})
```

---

# Auto-used fixtures

- Using auto-used fixtures defined in `conftest.py` 
  - Can lead to slower tests
  - Can lead to unexpected behaviour
  - Requires strict discipline

<v-clicks>

- In classes, auto-used fixtures are limited to a set of tests
  - Safer to use
  - Again, more explicit

</v-clicks>

---

# So why do I think classes are better for tests?

- Additional grouping choice 
- Smaller code footprint
- Reduced repetitions
- Explicit fixture availability
- Cleaner fixture namespace
- Safer auto-use of fixtures

---
layout: section
---

# Additional fixture scope

---

# Fixture scope

- By default, fixtures get created for each test that uses it
- In this example, the fixture `cat` will be created twice

```python
@pytest.fixture
def cat() -> Cat:
    return Cat()

def test_cat_meows(cat):
    assert cat.make_sound() == "mňau"
    
def test_cat_likes_fish(cat):
    assert cat.favourite_food() == Food.FISH
```

---

# Fixture scope

- The *scope* of a fixture can be modified to one of: `function`, `class`, `module`, `package` or `session`
- In this example, the fixture `cat` will be created just once

```python {1}
@pytest.fixture(scope="module")
def cat() -> Cat:
    return Cat()

def test_cat_meows(cat):
    assert cat.make_sound() == "mňau"

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
        assert cat.make_sound() == "mňau"

    def test_cat_likes_fish(self, cat):
        assert cat.favourite_food() == Food.FISH
```

---

# Fixture scope

- Primary benefit of appropriate scope is speed

<v-clicks>

- The slower a fixture is and the more tests use it, the bigger the benefit
- Once created, fixture remains active until all tests in scope finish
  - Can lead to unexpected behaviour, if the fixture has a side-effect (like DB insert)
  - Especially problematic with `autouse=True`


- Using classes enables using `class`-scoped fixtures, where tests in scope are limited
- In combination with `autouse=True` classes enhance posibilities of setup for a group of tests 

</v-clicks>


---

# Fixture scope

```python
@pytest.fixture
def cat(db):
    return Cat.objects.create()  # insert into DB

def test_cat_get_list(db, cat, api_client):
    response = api_client.get("/cat/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == cat.id

def test_cat_create(db, api_client):
    response = api_client.post("/cat/", {"name": "Micka"})
    assert response.status_code == 201
    assert Cat.objects.get().name == "Micka"
```

---

# Fixture scope

```python {8-11|1,16-17}
@pytest.fixture(scope="module")
def cat(db):
    return Cat.objects.create()  # insert into DB

def test_cat_get_list(db, cat, api_client):
    ...  # same as before

def test_cat_get_detail(db, cat, api_client):
    response = api_client.get(f"/cat/{cat.id}")
    assert response.status_code == 200
    ...

def test_cat_create(db, api_client):
    response = api_client.post("/cat/", {"name": "Micka"})
    assert response.status_code == 201
    # this will no longer work, becaue `cat` fixture scope is still active
    assert Cat.objects.get().name == "Micka"
```

<div v-click="2">

```text
FAILED test_cat.py::test_cat_create 
- Cat.MultipleObjectsReturned: get() returned more than one Cat -- it returned 2!
```

</div>

<!--

Only happens if both run.

The only solution here, if we want to keep `cat` module-scoped is to move to a separate file, or if the `cat`
fixture is in conftest.py, move to a different folder entirely. 

-->

---

# Fixture scope

```python
class TestCatRetrieve:
    @pytest.fixture(scope="class")
    def cat(self, db):
        return Cat.objects.create()  # insert into DB
    
    def test_get_list(self, cat, api_client):
        response = api_client.get("/cat/")
        ...
    
    def test_get_detail(self, cat, api_client):
        response = api_client.get(f"/cat/{cat.id}")
        ...

class TestCatCreate:
    def test_create(self, db, api_client):
        response = api_client.post("/cat/", {"name": "Micka"})
        assert response.status_code == 201
        assert Cat.objects.get().name == "Micka"
```

---

# So why do I think classes are better for tests?

- Additional grouping choice 
- Smaller code footprint
- Reduced repetitions
- Explicit fixture availability
- Cleaner fixture namespace
- Safer auto-use of fixtures
- Additional fixture scope

---

# Parametrizing test classes

```python
@pytest.mark.parametrize("cls,sound,food", [
    pytest.param(Cat, "mňau", Food.FISH, id="Cat"), 
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

<v-click>

```text
ERROR test_animal.py::TestAnimal - Failed: In test_sound: 
   function uses no argument 'food'
```

</v-click>

---

# Parametrizing test classes

```python {13,10|all}
@pytest.mark.parametrize("cls,sound,food", [
    pytest.param(Cat, "mňau", Food.FISH, id="Cat"), 
    pytest.param(Dog, "haf", Food.BONE, id="Dog"),
])
class TestAnimal:
    @pytest.fixture
    def animal(self, cls) -> Animal:
        return cls()
  
    def test_sound(self, animal, sound, food):
        assert animal.make_sound() == sound
  
    def test_favourite_food(self, animal, food, sound):
        assert animal.favourite_food() == food
```

<v-click>

- With each additional parameter and test this gets more and more annoying

</v-click>

---

# Parametrizing test classes

- What if the `Animal` initialisation is more complicated?

<v-click>

```python
@pytest.mark.parametrize("cls,animal_kwargs,sound,food", [
    pytest.param(Cat, {"name": "Micka"}, "mňau", Food.FISH, id="Cat"), 
    pytest.param(
        Dog, {"name": "Max", "breed": Breeds.LABRADOR}, 
        "haf", Food.BONE, id="Dog"
    ),
])
class TestAnimal:
    @pytest.fixture
    def animal(self, cls, animal_kwargs) -> Animal:
        return cls(**animal_kwargs)
  
    ...
```

</v-click>

---

# Parametrizing test classes

- What if passing static values isn't enough?

<v-click>

```python
@pytest.mark.parametrize("animal,sound,food,can_do_tricks", [
    # https://pypi.org/project/pytest-lazy-fixture/
    pytest.param(pytest.lazy_fixture("cat"), "mňau", Food.FISH, False, id="Cat"),
    pytest.param(pytest.lazy_fixture("dog"), "haf", Food.BONE, True, id="Dog"),
])
class TestAnimal:
    @pytest.fixture
    def cat(self) -> Cat:
        return Cat(name="Micka")
    
    @pytest.fixture
    def dog(self) -> Dog:
        dog = Dog(name="Max", breed=Breeds.LABRADOR)
        dog.teach_trick(Tricks.SHAKE_PAW)
        return dog
    
    def test_can_do_tricks(self, animal, food, sound, can_do_tricks):
        assert animal.can_do_tricks() == can_do_tricks
    ...
```

</v-click>

---
layout: section
---

# Abstract tests

---

# Abstraction as a mean of parametrisation

- We can use class inheritance to parametrize tests

<v-click>

```python {all|1|2-4|6-8|10-18}
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
```

</v-click>

---

# Abstraction as a mean of parametrisation

```python {all|1|5-7|2-3}
class TestCat(BaseAnimalTest):
    ANIMAL_SOUND = "mňau"
    FAVOURITE_FOOD = Food.FISH
  
    @pytest.fixture
    def animal(self) -> Cat:
        return Cat(name="Micka")
```

<v-click>

```text
test_cat.py::TestCat::test_sound PASSED           
test_cat.py::TestCat::test_favourite_food PASSED  
test_cat.py::TestCat::test_can_do_tricks PASSED   
```

</v-click>

---

# Abstraction as a mean of parametrisation

```python {all|1|6-10|2-4|12-13}
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
```

<v-click>

```text
test_dog.py::TestDog::test_sound PASSED                 
test_dog.py::TestDog::test_favourite_food PASSED        
test_dog.py::TestDog::test_can_do_tricks PASSED         
test_dog.py::TestDog::test_zoomies PASSED
```

</v-click>

---

# Abstraction as a mean of parametrisation

- Alternative method of parametrisation

<v-clicks>

- Suitable for a large number of parameters
- Suitable for when the parameters involve code rather than values

</v-clicks>

---

# Abstraction as a mean of parametrisation

### Example from Xelix

<v-clicks>

- Comment functionality on 8 classes of objects
  - Models and views essentially identically except for different foreign keys
- One base test class
  - 12 tests (list, create, validation, permissions, etc.)
  - 3 fixtures that need implementing (creating objects to comment on)
  - 4 parameters (class of object, foreign key name, urls, etc.)
  - 5 parameters with default values (number of queries on operation, etc.) 

</v-clicks>


---

# So why do I think classes are better for tests?

- Additional grouping choice 
- Smaller code footprint
- Reduced repetitions
- Explicit fixture availability
- Cleaner fixture namespace
- Safer auto-use of fixtures
- Additional fixture scope
- Alternative parametrisation of tests

---

# Conclusion

<v-clicks>

- Consider all options pytest gives you
- Using classes _can_ solve certain headaches when writing tests at scale
- There are many ways to accomplish the same thing
- In the end, any tests are better than no tests

</v-clicks>

---
layout: statement
---

# Questions?

---
layout: center
class: "text-center"
---

# Slides


<img src="/qr_link.png" style="height: 300px" />

[Web](https://www.mikulaspoul.cz/talks/pytest-classes-talk/) / [Source](https://github.com/mikicz/pytest-classes-talk/)
