# Jarvis assistant project

## Features

> STT and TTS are not implemented yet — the goal is to turn Jarvis into a
> vocal assistant, but for now it is a text-based chat interface.

- **Streamlit web UI** with a Jarvis-inspired theme (background, fonts, chat bar)
- **LLM chat** through Ollama with streaming responses
- **System prompt** that gives Jarvis its personality (`prompts/system_prompt.txt`)
- **Context window management** : token budget split between instructions and
  history, with automatic truncation of older messages when the limit is reached
- **Long-term memory** : conversation history stored in a SQL database
  (users, sessions, messages)
- **Facts memory** : knowledge graph powered by Graphiti + Neo4j to extract
  and store facts from conversations over time (service ready, not yet wired
  into the chat flow)
- **MVC architecture** with controllers orchestrating views and services

## Tech stack

| Technology | Why we use it |
|---|---|
| **Python 3.13** | Main language of the project |
| **Streamlit** | Build a web UI quickly without writing HTML/JS from scratch |
| **Ollama** | Run LLMs locally — no cloud API key needed for chat |
| **Pydantic + pydantic-settings** | Load and validate all settings from `.env` with types |
| **tiktoken** | Count tokens before each inference to stay within the model context window |
| **SQLAlchemy** | ORM to talk to the long-term memory database in Python |
| **Alembic** | Version and apply database schema changes (migrations) |
| **Neo4j** | Graph database to store facts, entities and relations |
| **Graphiti** | Library on top of Neo4j that extracts and evolves knowledge over time |
| **email-validator** | Validate user email format in the long-term memory service |

## Requirements

- Python 3.13
- [Ollama](https://ollama.com/) installed and running locally
- At least one chat model pulled (e.g. `ollama pull qwen3:8b`)
- An embedding model pulled if you use facts memory
  (e.g. `ollama pull nomic-embed-text`)
- [Neo4j](https://neo4j.com/download/) running locally (only needed for facts memory)
- Dependencies : `pip install -r requirement.txt`

## Configuration

All runtime settings live in a `.env` file at the project root.
They are loaded by `config/config.py` through pydantic-settings.

A template is provided : **`.env.example`**. Copy it to get started :

```bash
cp .env.example .env
```

Then edit `.env` with your own values. Here is what each variable does :

| Variable | Required | Description |
|---|---|---|
| `APP_ENV` | yes | `development` or `production` |
| `MODEL` | yes | Ollama model name for chat (e.g. `qwen3:8b`) |
| `THINK` | yes | `true` or `false` — enable model thinking if supported |
| `OLLAMA_PORT` | yes | Ollama server port (default `11434`) |
| `NB_CTX_TOKENS` | yes | Total context size sent to Ollama (`num_ctx`) |
| `NB_INSTRUCT_TOKENS` | yes | Token budget for system prompt, skills and rules |
| `NB_HISTORY_TOKENS` | yes | Token budget for chat history and user input |
| `EMBEDDER_MODEL` | yes | Ollama embedding model for Graphiti |
| `EMBEDDER_DIM` | yes | Embedding vector size (must match the model) |
| `LT_MEMORY_DATABASE_URL` | yes | SQL database URL for chat history |
| `FACTS_MEMORY_DATABASE_URL` | yes | Neo4j Bolt URL (e.g. `bolt://localhost:7687`) |
| `FACTS_MEMORY_USERNAME` | yes | Neo4j username |
| `FACTS_MEMORY_PASSWORD` | yes | Neo4j password |

> **Token budget rule** : `NB_INSTRUCT_TOKENS + NB_HISTORY_TOKENS` must be
> less than or equal to `NB_CTX_TOKENS`. If the chat history exceeds
> `NB_HISTORY_TOKENS`, `InferencePayload` drops the oldest messages
> automatically before calling the model.

> `SYSTEM_PROMPT` is **not** set in `.env`. It is loaded automatically from
> `prompts/system_prompt.txt` by `config/config.py`.

> `.env` is git-ignored. Never commit secrets. Only commit `.env.example`.

## Usage

- Open the app in your browser after launching Streamlit
- Type a message in the chat input at the bottom of the screen
- Jarvis streams its answer in real time
- The conversation is saved in the long-term memory database
- If the conversation gets too long, older messages are silently truncated
  to fit the token budget (Jarvis is informed via an internal system message)

## Start guide

### 1. Python environment

```bash
python -m venv venv
```

Activate the virtual environment :

- **Windows** : `.\venv\Scripts\activate`
- **Linux / macOS** : `source venv/bin/activate`

Install dependencies :

```bash
pip install -r requirement.txt
```

### 2. Configuration file

```bash
cp .env.example .env
```

Edit `.env` with your Ollama model, token budgets, ports and database credentials.

Tune the token values to match your model. Example for an 8k context model :

```env
NB_CTX_TOKENS=8192
NB_INSTRUCT_TOKENS=2048
NB_HISTORY_TOKENS=6144
```

### 3. Ollama

Make sure Ollama is running, then pull the models you configured :

```bash
ollama pull qwen3:8b
ollama pull nomic-embed-text
```

### 4. Databases

#### Long-term memory (SQL)

This database stores users, chat sessions and messages.

With the default SQLite URL (`sqlite:///./jarvis_memory.db`), apply migrations :

```bash
alembic upgrade head
```

This creates the `users`, `sessions` and `messages` tables.

> Before chatting, you need at least one user in the database. For now the
> UI uses a hardcoded email (`test@test.com`). Create the user manually or
> through `LTMemoryService.create_user()` until the user management UI is
> added.

#### Facts memory (Neo4j)

1. Install and start Neo4j locally
2. Set `FACTS_MEMORY_DATABASE_URL`, `FACTS_MEMORY_USERNAME` and
   `FACTS_MEMORY_PASSWORD` in your `.env`
3. Graphiti will create its indices automatically on first connection
   (`facts_database/bootstrap.py`)

### 5. Launch the app

```bash
python -m streamlit run app.py
```

> Make sure you run the command with the Python from your virtual environment.

## Dev guide

### Architecture

The project follows a **MVC** pattern :

- **Model** → `services/` + `models/` + `lt_database/` + `facts_database/` :
  business logic and data access
- **View** → `views/` : everything the user sees (Streamlit UI)
- **Controller** → `controllers/` : orchestrates views and services (e.g.
  saves messages, calls the LLM, updates session state)

Each view implements the `View` interface from `interfaces/view.py`.
Every view exposes a `render()` method — that is all you need to call to
display it.

`helpers/st_session_helper.py` centralises Streamlit session state
(current chat session id, message history, truncation counter).

`models/inference_payload.py` builds the list of messages sent to Ollama.
It splits the payload into two parts :

- **instructs** — system prompt, skills, rules (fixed budget : `NB_INSTRUCT_TOKENS`)
- **history** — past messages and current user input (budget : `NB_HISTORY_TOKENS`)

`async_worker.py` runs an asyncio event loop in a background thread so
synchronous Streamlit code can call async Graphiti/Neo4j operations.

### How it works

When you launch the app :

1. **Streamlit** runs `app.py`
2. `STSessionHelper` initialises session state (`chat_session_id`,
   `chat_history`, `nb_cut_session_msgs`)
3. `MainWindow` sets the page config, background and global styles
4. `ChatView` displays the message history from session state
5. `BottomView` renders the bottom bar with the chat input (`ChatBarView`)
6. When the user sends a message :
   - `ChatBarView` calls `ChatController.ask_llm_response()`
   - the controller loads history from the SQL database via `LTMemoryService`
   - `LLMService` builds an `InferencePayload`, adds the history and the new
     user message, and counts tokens with **tiktoken**
   - if the history exceeds `NB_HISTORY_TOKENS`, the oldest messages are
     dropped and a system note is added so Jarvis knows the session was truncated
   - Ollama streams a response (with `num_ctx` set to `NB_CTX_TOKENS`)
   - user and assistant messages are saved back to the database
   - session state is updated so the view can display the new history
7. `FactsMemoryService` (Graphiti + Neo4j) exists in `services/` but is not
   yet called from the chat controller — integration is still in progress

Think of it like Russian dolls : each view can create smaller views inside
itself. `app.py` only knows about `MainWindow`.

### File structure

```text
jarvis/
├── app.py                          # Entry point — initialises session, launches UI
├── async_worker.py                 # Background asyncio thread for Graphiti calls
├── requirement.txt                 # Python dependencies with versions
├── alembic.ini                     # Alembic config for SQL migrations
├── README.md
├── .env.example                    # Template for environment variables (copy to .env)
├── .gitignore
├── .cursorignore
├── .env                            # Local secrets (not versioned — create from .env.example)
│
├── .streamlit/
│   └── config.toml                 # Streamlit theme, fonts and server options
│
├── config/
│   └── config.py                   # Loads and validates all settings from .env
│
├── interfaces/
│   └── view.py                     # Base interface — every view implements render()
│
├── controllers/
│   └── chat_controller.py          # Orchestrates chat flow (LLM + memory + session)
│
├── services/
│   ├── llm_service.py              # Builds InferencePayload, streams from Ollama
│   ├── lt_memory_service.py        # Users, sessions and messages (SQL)
│   └── facts_memory_service.py     # Facts extraction and search (Graphiti + Neo4j)
│
├── models/
│   ├── user.py                     # Pydantic model for user data (domain layer)
│   └── inference_payload.py        # Token counting, history window and message assembly
│
├── helpers/
│   └── st_session_helper.py        # Centralised Streamlit session state
│
├── lt_database/                    # Long-term memory (SQL)
│   ├── base.py                     # SQLAlchemy declarative base
│   ├── bootstrap.py                # Engine and session factory
│   ├── orm/
│   │   ├── user.py                 # User table
│   │   ├── session.py              # Chat session table
│   │   └── message.py              # Message table
│   └── migrations/                 # Alembic migration scripts
│       ├── env.py
│       └── versions/
│
├── facts_database/
│   └── bootstrap.py                # Graphiti + Neo4j initialisation
│
├── views/
│   ├── mainwindow.py               # Root view — background, page config
│   ├── chat_view.py                # Displays chat history
│   └── bottom_bar/
│       ├── bottom_view.py          # Bottom bar layout (mic + chat input)
│       └── chat_bar_view.py        # Chat input and streaming response display
│
├── prompts/
│   └── system_prompt.txt           # Jarvis personality, tone and safety rules
│
└── static/                         # Images and fonts served by Streamlit
    ├── fonts/
    │   └── orbitron.light.ttf
    └── images/
        ├── jarvis_background.png
        ├── jarvis_background_blurry.png
        └── jarvis_logo.png
```

---
Alzaix Florian
