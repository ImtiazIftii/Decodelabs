# Rule-Based AI Chatbot (SON / Aria)

A deterministic, zero-dependency rule-based conversational agent built with pure Python control flow and data structures. Developed as **Project 1** for the **DecodeLabs AI Internship**.

---

## 📌 Project Overview

In an era dominated by Large Language Models (LLMs), deterministic rule-based systems remain foundational. Real-world AI production systems rely heavily on deterministic guardrail layers (e.g., input sanitization, intent classification, safety boundaries, and guaranteed fallbacks) wrapped around probabilistic generative models.

This project implements that fundamental "logic engine" from first principles:
- **Zero external dependencies**: Built entirely using Python standard libraries (`random`, `typing`).
- **Deterministic control**: Full auditability with no hallucination risk.
- **Traceable execution**: Direct mapping from sanitized input to matched intent and corresponding response.

---

## 🏗️ Architecture (IPO Model)

The chatbot operates on a classic **Input-Process-Output (IPO)** architecture:

```
[ User Input ]
      │
      ▼
┌─────────────────────────┐
│ 1. Input & Sanitization │ ──> Lowercase, strip whitespace, guard against empty input
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ 2. Intent Matching      │ ──> Substring keyword scan across knowledge base intents
└─────────────────────────┘
      │
      ├──> Intent Matched  ──> Sample from intent response pool (`random.choice`)
      └──> No Match Found  ──> Sample from fallback responses pool
      │
      ▼
┌─────────────────────────┐
│ 3. Output & Logging     │ ──> Log turn in `conversation_log`, display response to user
└─────────────────────────┘
```

---

## ✨ Features

- **Robust Input Sanitization**: Normalizes inputs by trimming whitespace and converting to lowercase so variations like `"  Hello "` and `"hELLo"` match cleanly.
- **Substring Keyword Matching**: Matches intents based on keyword inclusion rather than fragile exact-string comparisons (e.g., `"hello there"` matches `"hello"`).
- **Varied Dynamic Responses**: Uses response pools paired with `random.choice()` to ensure conversational variety without repetitive responses.
- **Graceful Session Termination**: Recognizes exit commands (`"exit"`, `"quit"`, `"bye"`, `"goodbye"`) to cleanly close conversation loops.
- **Guaranteed Fallback**: Handles out-of-scope or unmapped queries gracefully using predefined fallback responses.
- **Conversation Audit Log**: Keeps a record of all conversation pairs `(user_input, bot_response)` in `self.conversation_log`.

---

## 🧠 Knowledge Base Intents

The chatbot comes preconfigured with modular intent domains:

| Intent | Sample Triggers | Description |
|---|---|---|
| `greeting` | `hello`, `hi`, `hey`, `hola`, `greetings` | Welcome greetings |
| `farewell` | `bye`, `goodbye`, `see you`, `later` | Closing statements |
| `thanks` | `thanks`, `thank you`, `appreciate it` | Expressions of gratitude |
| `identity` | `who are you`, `what are you`, `your name` | Bot identity and purpose |
| `capability` | `what can you do`, `help`, `commands` | Feature guide and usage instructions |
| `mood` | `how are you`, `how're you`, `how you doing` | Bot status check |
| `assurance` | `understood`, `got it`, `nice` | Acknowledgments |
| `checkup` | `what about you`, `wbu`, `how you doing` | Reciprocal check-ins |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher installed.

### Running the Chatbot

Clone the repository and run `chatbot.py` directly:

```bash
python chatbot.py
```

### Example Session

```text
SON: Hello! I'm SON, your rule-based assistant. Type 'exit' to end our chat.

You: hello
SON: Hey there! I'm SON. How can I help you today?
You: what can you do
SON: I can chat about greetings, farewells, and a bit about myself. Type 'exit' or 'bye' any time to leave.
You: who are you
SON: I'm SON, a rule-based chatbot built with pure control flow logic — no machine learning here, just clean decision-making.
You: understood
SON: Glad you got it
You: bye
SON: Goodbye! It was nice chatting with you.
```

---

## 🧪 Running Unit Tests

Unit tests verify input sanitization, intent matching, response pooling, and logging:

```bash
python -m unittest discover -s rule-based-chatbot/tests -v
```

---

## 📂 Project Structure

```text
.
├── chatbot.py                      # Main RuleBasedChatbot class and interactive CLI loop
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore file for archives and PDFs
└── rule-based-chatbot/
    ├── chatbot.py                  # Packaged reference implementation
    ├── README.md                   # Module-level documentation
    └── tests/
        └── test_chatbot.py         # Automated unit test suite
```

---

## 💡 Engineering & Design Decisions

1. **Object-Oriented Design (`RuleBasedChatbot` Class)**:
   Wrapping logic inside a dedicated class decouples the response engine (`get_response`) from the CLI interface (`run`). This allows `RuleBasedChatbot` to be easily imported into web APIs (Flask/FastAPI), UI frontends, or automated test suites.
2. **Dictionary-Based Routing vs. `if/elif` Chains**:
   Hardcoded `if/elif` ladders become unmaintainable as rules scale ($O(N)$ code complexity). Storing intents as structured dictionary data decouples the knowledge base from the execution logic, allowing dynamic intent additions without modifying code branches.
3. **Substring Matching over Exact Matching**:
   A naive exact match (`dict.get(raw_input)`) fails whenever punctuation, extra words, or phrasing variations are introduced. Scanning triggers as substrings balances simplicity with conversational flexibility.

---

