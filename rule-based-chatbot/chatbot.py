"""
Rule-Based AI Chatbot
=====================
DecodeLabs AI Internship — Project 1

A deterministic, rule-based chatbot built entirely from control flow and
dictionaries — no machine learning involved. This is the "logic engine"
that every generative AI system still relies on underneath: input
sanitization, intent matching, and a guaranteed fallback for the unknown.

Architecture (IPO model):
    INPUT   -> sanitize the raw text (lowercase, strip whitespace)
    PROCESS -> match sanitized text against a knowledge base of intents
    OUTPUT  -> return a response, or a fallback if nothing matched

Author: Ifti
"""

from __future__ import annotations

import random
from typing import Optional


class RuleBasedChatbot:
    """A simple rule-based chatbot that matches user input against a
    predefined knowledge base of intents and returns an appropriate,
    slightly-varied response.

    This deliberately avoids exact-string dictionary lookups (the naive
    `responses.get(user_input)` approach) in favor of keyword/substring
    matching, so "hello there" still matches the "greeting" intent even
    though it isn't an exact key. That single design choice is what keeps
    the bot from feeling brittle.
    """

    def __init__(self, bot_name: str = "Aria") -> None:
        self.bot_name = bot_name
        self.conversation_log: list[tuple[str, str]] = []

        # --- Knowledge base -------------------------------------------------
        # Each intent maps a set of trigger keywords to a pool of possible
        # responses. Using a pool (rather than one fixed string) plus
        # random.choice() gives the bot a bit of personality instead of
        # repeating itself verbatim every time.
        self.knowledge_base: dict[str, dict[str, list[str]]] = {
            "greeting": {
                "triggers": ["hello", "hi", "hey", "hola", "greetings"],
                "responses": [
                    f"Hey there! I'm {bot_name}. How can I help you today?",
                    "Hello! Great to see you.",
                    "Hi! What's on your mind?",
                ],
            },
            "farewell": {
                "triggers": ["bye", "goodbye", "see you", "later"],
                "responses": [
                    "Goodbye! Have a great day.",
                    "See you next time!",
                ],
            },
            "thanks": {
                "triggers": ["thanks", "thank you", "appreciate it"],
                "responses": ["You're welcome!", "Anytime!"],
            },
            "identity": {
                "triggers": ["who are you", "what are you", "your name"],
                "responses": [
                    f"I'm {bot_name}, a rule-based chatbot built with pure "
                    "control flow logic — no machine learning here, just "
                    "clean decision-making."
                ],
            },
            "capability": {
                "triggers": ["what can you do", "help", "commands"],
                "responses": [
                    "I can chat about greetings, farewells, and a bit about "
                    "myself. Type 'exit' or 'bye' any time to leave."
                ],
            },
            "mood": {
                "triggers": ["how are you", "how're you", "how you doing"],
                "responses": [
                    "I'm just a set of if-else rules, but I'm running "
                    "smoothly! How about you?"
                ],
            },
            "assurance":{
                "triggers":["understood","got it","nice"],
                "responses":[
                    "Nice!"
                    "Glad you got it"
                    "Great"
                ],
            },
            "checkup":{
                "triggers":["What about you?","wbu","How you doing"],
                "responses":[
                    "Doing great! Thanks for asking"
                    "Better"
                    "Can't complain cause I actually can't"
                    "TungtungtungSahur = I am doing good :)"
                ]
            }
        }

        self.exit_commands = {"exit", "quit", "bye", "goodbye"}
        self.fallback_responses = [
            "I don't quite understand that yet. Could you rephrase?",
            "Hmm, that's outside my current rule set. Try asking something else.",
            "I'm not trained on that — I only know my predefined rules for now.",
        ]

    # --- Phase 1: Input & Sanitization --------------------------------------
    @staticmethod
    def sanitize(raw_input: str) -> str:
        """Normalize user input: lowercase and strip whitespace.

        Without this, 'Hello', 'hello', and '  hello  ' would all be
        treated as distinct, unmatched inputs.
        """
        return raw_input.lower().strip()

    # --- Phase 2: Process / Intent matching ---------------------------------
    def match_intent(self, clean_input: str) -> Optional[str]:
        """Scan the knowledge base for the first intent whose keyword
        appears anywhere in the sanitized input.
        """
        for intent, data in self.knowledge_base.items():
            for trigger in data["triggers"]:
                if trigger in clean_input:
                    return intent
        return None

    # --- Phase 3: Output / Response generation ------------------------------
    def get_response(self, raw_input: str) -> str:
        """Full pipeline: sanitize -> match -> respond. This is the
        function a test suite (or another script importing this class)
        should call directly.
        """
        clean_input = self.sanitize(raw_input)

        if not clean_input:
            return "Say something — I'm listening!"

        intent = self.match_intent(clean_input)
        if intent:
            response = random.choice(self.knowledge_base[intent]["responses"])
        else:
            response = random.choice(self.fallback_responses)

        self.conversation_log.append((raw_input, response))
        return response

    def should_exit(self, clean_input: str) -> bool:
        """Check whether the sanitized input is a recognized exit command."""
        return clean_input in self.exit_commands

    # --- The heartbeat: continuous loop --------------------------------------
    def run(self) -> None:
        """Start the interactive conversation loop. Runs until the user
        issues an exit command — the 'kill command' that breaks the loop.
        """
        print(
            f"{self.bot_name}: Hello! I'm {self.bot_name}, your rule-based "
            "assistant. Type 'exit' to end our chat.\n"
        )

        while True:
            raw = input("You: ")
            clean = self.sanitize(raw)

            if self.should_exit(clean):
                print(f"{self.bot_name}: Goodbye! It was nice chatting with you.")
                break

            reply = self.get_response(raw)
            print(f"{self.bot_name}: {reply}")


if __name__ == "__main__":
    bot = RuleBasedChatbot(bot_name="Aria")
    bot.run()
