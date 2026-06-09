# Jarvis assistant project

---

## Features

For now there are only a few features:
- LLM interaction through terminal
- Base system prompt to feel like its actually Jarvis

## Requirements

- Python3.13
- `pip install -r requirements.txt`
- Ollama installed with for now qwen3:8b installed

## Usage

- Interacts in the cli with the assistant

## Start guide

Command : `python app.py`

> Note it depends if the dependencies are installed in the virtual
environnement or in the global Python. Make sure to execute it with
the right version of your python.

Safe run if problems with Python environnement:
- First create the virtual env : `python -m venv venv`
- Activate the env : `./venv/Scripts/activate` (to adapt to windows/linux/macos)
- Install dependencies : `pip install -r requirements.txt`
- Launch using: `python main.py`

## Dev guide

---

### Architecture

For now it is a basic MVC architecture to move fast with the project.

### File structure

jarvis/
├── app.py # Main
├── requirement.txt # Python dependencies list with VERSIONS
├── README.md
├── .gitignore
├── .cursorignore
├── .env # Where the global constants are stored. To be created to edit the
global parameters of the program. Read the config/config.py file to have the
list of parameters to set.
├── config/
│   └── config.py # Stores the config using BaseSettings from pydantic
├── services/ # All the classes of code that contains domain functions logic
│   └── llm_service.py
└── prompts/ # Contains all the text prompts for the llm
    └── system_prompt.txt