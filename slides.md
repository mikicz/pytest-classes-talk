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
