# Developer Assistant Agent

A learning project built to understand, end-to-end, how a real LLM agent is put together: prompting, tool use, structured output validation, and shipping the result behind both a CLI and a web UI. It's an AI agent that takes a developer's request (and optional code/context) and returns a structured, actionable report — explaining code, spotting bugs, or planning a feature, without ever executing the user's code.

---
## Demo
 
![Developer Assistant Agent Demo](assets/demo.gif)
 
*The Streamlit app taking a developer request and code snippet, and returning a structured report with task type, difficulty, risk level, potential bugs, and next steps.*
 
---

## 1. Problem Statement

Developers constantly ask the same categories of questions when working with unfamiliar or messy code:

- *"What does this code actually do?"*
- *"Why might this be broken?"*
- *"How should I approach adding this feature?"*
- *"Is this safe to act on, or should I get a second pair of eyes on it?"*

A plain chatbot can answer these in free text, but free text is hard to build tooling on top of — you can't reliably route it, log it, score its risk, or render it consistently in a UI. What's actually needed is a system that:

1. Understands *what kind* of developer task it's looking at (explanation vs. debugging vs. planning vs. general Q&A).
2. Can inspect code with real tools instead of guessing (e.g., actually parsing Python rather than eyeballing it).
3. Returns a **predictable, structured** answer — not an essay — so it can be rendered identically whether it's printed to a terminal or displayed in a dashboard.
4. Is honest about uncertainty and flags when a human should double check the output, rather than presenting every answer with false confidence.

**Goal:** build a small, well-scoped agent that solves this reliably, and use it as a vehicle to learn the core mechanics of modern LLM application development — prompting, tool calling, and structured output — rather than relying on a framework's defaults without understanding them.

---

## 2. Solution

The Developer Assistant Agent is a LangChain-based agent (powered by Google's Gemini 2.5 Flash) that:

1. Takes a **developer request** and optional **code/context** as input.
2. Runs through a system prompt that scopes its role strictly: explain code, debug, plan features, or answer general programming questions — and explicitly instructs it *not* to invent bugs or execute code.
3. Has access to a **real static-analysis tool** (`check_python_syntax`, built on `parso`) to check Python syntax without ever running user code.
4. Is forced, via LangChain's structured output support, to return its answer in a fixed **Pydantic schema** (`DeveloperTaskReport`) — no matter what the underlying model generates, the app always receives the same shape of data back.
5. Is exposed through two interfaces built on the exact same core logic:
   - A **CLI app**, for quick terminal-based use.
   - A **Streamlit web app**, for a richer visual report (metrics, expandable bug details, raw JSON view).

### High-level flow

```
User request + optional code
            │
            ▼
  build_developer_user_message()   →  formats input into a single prompt
            │
            ▼
        LangChain agent
   (Gemini 2.5 Flash + system prompt)
            │
            ├── may call → check_python_syntax(code)  [tool]
            │
            ▼
  Structured output enforced against
       DeveloperTaskReport (Pydantic)
            │
            ▼
   CLI app  ──or──  Streamlit app
   (render the same report differently)
```

### Project structure

```
Developer-Assistant-Agent/
├── src/
│   ├── config.py      # Model loading (Gemini via API key, with a commented-out local Ollama option)
│   ├── prompts.py      # System prompt + user message builder
│   ├── schemas.py      # Pydantic schema the agent's output must conform to
│   ├── tools.py        # Tool(s) the agent can call (Python syntax checker via parso)
│   └── agent.py         # Wires model + prompt + tools + schema into a runnable agent
├── apps/
│   ├── cli_app.py       # Terminal interface
│   └── streamlit_app.py # Web interface
├── examples/                    # Example inputs/outputs
└── requirements.txt
```

### The structured output schema

Every response — regardless of task type — is validated against this shape:

| Field | Type | Purpose |
|---|---|---|
| `task_type` | enum | `code_explanation`, `debugging`, `feature_planning`, `general_question` |
| `difficulty` | enum | `easy`, `medium`, `hard` |
| `risk_level` | enum | `low`, `medium`, `high` — how risky it'd be to act without review |
| `summary` | string | Plain-language summary of the analysis |
| `key_points` | list[str] | Notable observations |
| `potential_bugs` | list[PotentialBug] | Each with a `bug` description and an `explanation` |
| `next_steps` | list[str] | Concrete actions for the developer |
| `needs_human_review` | bool | Explicit flag for when the model isn't confident enough to be trusted blindly |

This is the core design decision of the project: instead of trusting the LLM to format things consistently, the schema *is* the contract. If the model's output doesn't fit, LangChain's structured output layer handles the enforcement — the app code never has to parse free text.

---

## 3. Skills Demonstrated

This project was used deliberately as a hands-on way to build and practice the following:

**LLM application engineering**
- Designing a scoped, constraint-driven **system prompt** (explicit dos/don'ts: don't invent bugs, don't execute code, use tools only when useful).
- Working with **LangChain's agent abstraction** (`create_agent`) end-to-end rather than just calling a chat model directly.
- Enforcing **structured output** from an LLM using Pydantic schemas, including nested models (`PotentialBug` inside `DeveloperTaskReport`) and constrained `Literal` enum fields.
- Implementing a **custom LangChain tool** (`@tool`) that wraps a real static-analysis library (`parso`) instead of relying on the model's own (unreliable) judgment about syntax.
- Handling **provider swapping** — the config layer supports both a hosted API model (Gemini) and a local model (Ollama/Llama 3.1), demonstrating an understanding of how to decouple agent logic from a specific model provider.

**Software engineering practices**
- Clean **separation of concerns** across config, prompts, schemas, tools, and agent orchestration — each in its own module.
- Building **two independent front ends** (CLI, Streamlit) on top of one shared `run_agent()` core, avoiding duplicated business logic.
- Defensive coding: explicit checks for missing API keys, graceful handling when the agent fails to return a structured response, and try/except boundaries around user-facing calls in the Streamlit app.
- Environment-based configuration via `python-dotenv`, keeping secrets out of source control.

**Product/UX thinking**
- Translating a structured data object into two different experiences: a readable terminal printout, and a Streamlit dashboard with metrics, collapsible bug explanations, and a raw JSON debug view.
- Designing the schema itself as a UX decision — `risk_level` and `needs_human_review` exist specifically so the interface can visually flag when a user shouldn't trust the output blindly.

---

## 4. Setup & Usage

### Requirements
```bash
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```
(Alternatively, uncomment the Ollama block in `src/config.py` to run fully locally with `llama3.1:8b` instead of calling out to Gemini.)

### Run via CLI
```bash
python -m apps.cli_app
```
You'll be prompted for a request and, optionally, code/context to analyze.

### Run via Streamlit
```bash
streamlit run apps/streamlit_app.py
```
This opens a browser UI where you can submit a request, paste code, and view the full structured report — task type, difficulty, risk level, key points, potential bugs, and next steps.

---

## 5. Future Improvements

- **Expand the toolset** beyond syntax checking — e.g., linting (`pylint`/`ruff`), complexity analysis, or dependency/import checks, so the agent's bug-finding is backed by more than one signal.
- **Multi-language support** — currently the only real tool (`check_python_syntax`) is Python-specific; the schema and prompt are language-agnostic but the tooling isn't yet.
- **Automated evaluation** — fill in `docs/evaluation.md` with a small test set of known-buggy snippets and expected `task_type`/`risk_level` outputs to track regressions as the prompt or model changes.
- **Better error surfacing** — right now a missing structured response raises a generic `RuntimeError`; this could be made more diagnostic (e.g., surfacing the model's raw text so failures are easier to debug).
- **Conversation memory** — support multi-turn follow-ups ("now check this related file") instead of treating every request as a single isolated call.
- **Severity field on bugs** — the Streamlit app already has UI logic ready for a `severity` attribute on `PotentialBug` that doesn't exist in the schema yet; wiring this up would let bug reports be sorted/filtered by urgency.
- **Test coverage** — no automated tests currently exist for `src/`; adding unit tests around the schema validation and tool logic would harden the project against regressions.

---

## 6. Tech Stack

`Python` · `LangChain` · `Google Gemini 2.5 Flash` (or local `Ollama` / `Llama 3.1`) · `Pydantic` · `parso` · `Streamlit` · `python-dotenv`
