# Rule-Based AI Chatbot

A deterministic, zero-dependency chatbot built entirely from control flow and
dictionaries — no machine learning involved. This is Project 1 of the
DecodeLabs AI Engineering track: the "logic engine" phase.

## Why a rule-based bot, in the age of LLMs?

Every modern LLM-powered product still sits on top of rule-based logic —
input filtering, intent routing, and safety guardrails (frameworks like
NVIDIA NeMo Guardrails and Llama Guard are exactly this pattern) are
deterministic control layers wrapped around a probabilistic core. This
project builds that control layer from first principles: no hidden
weights, no hallucination risk, fully traceable input → logic → output.

## How it works

```
INPUT  -> sanitize (lowercase, strip whitespace)
PROCESS -> match sanitized text against a knowledge base of intents
OUTPUT -> return a response, or a fallback if nothing matched
```

Matching is **keyword-based** (a trigger word anywhere in the sentence),
not exact-string matching — so `"hello there"` still matches the greeting
intent even though the full sentence was never explicitly defined as a key.
Each intent maps to a *pool* of responses, selected with `random.choice()`,
so the bot doesn't repeat itself verbatim on every turn.

## Running it

```bash
python chatbot.py
```

```
Aria: Hello! I'm Aria, your rule-based assistant. Type 'exit' to end our chat.

You: hi
Aria: Hey there! I'm Aria. How can I help you today?
You: what can you do
Aria: I can chat about greetings, farewells, and a bit about myself...
You: exit
Aria: Goodbye! It was nice chatting with you.
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```
rule-based-chatbot/
├── chatbot.py           # RuleBasedChatbot class + CLI entry point
├── tests/
│   └── test_chatbot.py  # unit tests for sanitization, matching, responses
├── README.md
└── .gitignore
```

## Design notes

- **Why a class, not a script?** Wrapping the bot in `RuleBasedChatbot`
  makes the response engine (`get_response`) independently testable and
  reusable — another script could `import` it without triggering the
  interactive loop.
- **Why `dict` lookup over `if/elif` chains?** An if-elif ladder scales
  linearly (O(n)) with the number of rules and becomes a maintenance
  liability. Dictionary-based intent lookup keeps matching fast and the
  knowledge base easy to extend — just add a new key, no new branches.

## Future work

- Swap exact/substring matching for semantic similarity (embeddings) —
  the natural next step from Project 1's "discrete mapping" to a
  "continuous mapping" model.
- Add simple conversational state (e.g., remembering the user's name
  across turns).
- Persist conversation logs to a file for session review.

## Author

Ifti
