# CodesOfEmpires

A project that aimed to be a 2D game, with mostly Age Of Empires mechanics, BUT the units can only move through Python code!

This project is **Abandoned** in all possible ways! Someone made (kind of) the same game, that actually works - **[yare.io](yare.io)**.

----
### The ideas

#### Implemented

Players submit their code in 3 snippets - `constants`, `function` and `runtime`. Constants is supposed to contain only variable definitions (e.g. `NUMBER_OF_ATTACKING_UNITS=7`),
function can contain function definitions (something like an STDLIB that every player could make), and the runtime that runs in a `while True` loop *for each unit*.

Worker Units gather Wood, Food and Iron and can create more Worker units that automatically start running the given player code.

#### Not implemented

Units like Archers (need more Wood), Cavalry (need more food) and infantry (need more iron) was planned to be available.
The military units follow a Pokemon Starter-style cycle of weaknesses (Cavalry > Archers > Infantry > Cavalry).

----

### Why I stopped working on it

I am mainly working as SecDevOps (and this makes me creates abominations [like this](https://github.com/operatorequals/KubeWars)), so I don't have
time and mental capacity to debug in-depth Python and Pyglet threading issues.

If you feel like it, please fork it and continue working on it! I can happilly provide all insight I have in this code base (models, `update` stuff, etc)

----


To run the tests go with (only `master` branch works!):
```python
pip install -r requirements.txt
python -m unittest discover tests/
```

