# Cowabunga

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) 

Help the cows cross the river safely!
The game can be played online in browser or locally with Pygame.
[PLAY IN BROWSER](https://nicolapesaresi.github.io/Cowabunga/)

![example_screenshot](cowabunga/py_game/assets/_example_screenshot.png)

Cowabunga is an amazing iOS game created by Mark Andrade. This repository is just the Pygame recreation of the game made by a fan. All credits for the original idea and game go to Mark Andrade and AndradeArts.

🌐 [Mark Andrade website](https://markandrade.com)
👔 [Mark Andrade LinkedIn](https://www.linkedin.com/in/markandrade/)

## Game
Cows are coming from the left side of the screen and have to cross a river. You can help by bouncing them on your lifeboat to the other side. Each cow needs three bounces to cross the river. You have 3 lives to try and save as many as you can.

## Structure
The repository is structured as follows:
- In the `cowabunga/env` folder you can find the game environment. This defines the game rules and logic. This is separate from the pygame interface as I intend to train a Reinforcement Learning agent on the game in the future.
- In the `cowabunga/py_game` folder there is the pygame interface for the game env and the assets for the sprites.
- `cowabunga/scripts/run_pygame.py` is the script that makes you play the game on desktop.
- `main.py` is the script that is used by Pygbag to handle pygame in the browser.

Development of the game is ongoing. Sounds and cow sequences will be added soon. 

## Installation
The repository is setup us as a poetry project and by default requires Python 3.10 or later.
To install the repository you can follow these steps:

First, install `poetry` if you haven't already, as indicated by the instructions on the [Poetry installation page](https://python-poetry.org/docs/).
Then, clone the repository to your local machine using the following command:
```
git clone https://github.com/nicolapesaresi/Cowabunga
cd Cowabunga
```
Create and activate a virtual environment:
```
# replace `myenv` with the name of your virtual environment
python3 -m venv myenv
source myenv/bin/activate
```
Or, if using `Conda`:
```
conda create -n myenv python=3.10
conda activate myenv
```
Use Poetry to install the project dependencies:
```
poetry install
```
Now you can run the game on desktop with:
```
python cowabunga/scripts/run_pygame.py
```

## Development
The game is created with Pygame, and is playable in browser using Pygbag and Github Pages.
Modifications to the game loop have to be replicated in both `PygameRenderer.run()` and `main.py`, to work both locally and in browser.
Adding modifications to the game requires to install dev dependencies with 
```
poetry install --with dev
```
To test browser functionalities, the game can be run on localhost with the command 
```
pygbag .
```
After testing the changes, they can be deployed in github pages with
```
make publish
```

## Resources
[Pygame documentation](https://www.pygame.org/docs/)
[Pygbag](https://github.com/pygame-web/pygbag)
[Pygbag documentation](https://pygame-web.github.io/wiki/pygbag/)
[Hosting Pygame games with github pages](https://github.com/league-curriculum/Python-Web-Game?tab=readme-ov-file)
[Mark Andrade website](https://markandrade.com)
[Mark Andrade LinkedIn](https://www.linkedin.com/in/markandrade/)