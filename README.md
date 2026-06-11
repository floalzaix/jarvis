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

Command : `python -m streamlit run app.py`

> Note it depends if the dependencies are installed in the virtual
environnement or in the global Python. Make sure to execute it with
the right version of your python.

Safe run if problems with Python environnement:
- First create the virtual env : `python -m venv venv`
- Activate the env : `./venv/Scripts/activate` (to adapt to windows/linux/macos)
- Install dependencies : `pip install -r requirements.txt`
- Launch using: `python -m streamlit run app.py`

## Dev guide

---

### Architecture

The project follows a simple **MVC** pattern to move fast while keeping
the code easy to read:

- **Model** → `services/` : business logic (for example, talking to the LLM)
- **View** → `views/` : everything the user sees in the browser (Streamlit UI)
- **Controller** → not added yet ; for now, views call services directly

Each view implements the `View` interface from `interfaces/view.py`.
Every view has a `render()` method : that is the only method you need to
call to display it on screen.

### How it works

When you launch the app, here is what happens step by step:

1. **Streamlit** starts and runs `app.py`
2. `app.py` creates a `MainWindow` and calls `render()`
3. `MainWindow` sets the page title, background image and global styles
4. It then creates a `BottomView` and calls `render()` on it too
5. `BottomView` splits the bottom bar into two columns :
   - left → `ToolsView` (tool buttons, like the microphone)
   - right → `ChatView` (chat input and messages)
6. When the user sends a message, `ChatView` will call `services/llm_service.py`
   to get a response from Ollama (this wiring is still in progress)

Think of it like Russian dolls : each view can create smaller views
inside itself. `app.py` only knows about `MainWindow` ; it does not need
to know the details of the chat or tools.

### File structure

```text
jarvis/
├── app.py                      # Entry point — launches the Streamlit app
├── requirement.txt             # Python dependencies list with versions
├── README.md
├── .gitignore
├── .cursorignore
├── .env                        # Local config (not versioned). Create this
│                               # file to override default settings. See
│                               # config/config.py for available parameters.
│
├── .streamlit/
│   └── config.toml             # Streamlit theme, fonts and server options
│
├── config/
│   └── config.py               # Loads settings from .env with pydantic
│
├── interfaces/
│   └── view.py                 # Base interface — every view must implement
│                               # render()
│
├── services/                   # Business logic (the "Model" part)
│   └── llm_service.py          # Sends messages to Ollama and streams the
│                               # response
│
├── views/                      # UI components (the "View" part)
│   ├── mainwindow.py           # Root view — background, page config
│   └── bottom_bar/
│       ├── bottom_view.py      # Layout of the bottom bar (two columns)
│       ├── chat_view.py        # Chat messages and input field
│       └── tools_view.py       # Side buttons (microphone, etc.)
│
├── prompts/                    # Text prompts sent to the LLM
│   └── system_prompt.txt       # Defines Jarvis personality and behaviour
│
└── static/                     # Images and fonts served by Streamlit
    ├── fonts/
    │   └── orbitron.light.ttf  # Custom font used in the UI theme
    └── images/
        ├── jarvis_background.png
        └── jarvis_logo.png
```