"""
Unit tests for RuleBasedChatbot.

Run with:
    python -m unittest discover -s tests
"""

import sys
import os
import unittest

# Make the parent directory importable when running this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chatbot import RuleBasedChatbot


class TestSanitize(unittest.TestCase):
    def test_lowercases_and_strips(self):
        self.assertEqual(RuleBasedChatbot.sanitize("  HeLLo  "), "hello")

    def test_empty_string(self):
        self.assertEqual(RuleBasedChatbot.sanitize("   "), "")


class TestIntentMatching(unittest.TestCase):
    def setUp(self):
        self.bot = RuleBasedChatbot(bot_name="TestBot")

    def test_greeting_exact_match(self):
        self.assertEqual(self.bot.match_intent("hello"), "greeting")

    def test_greeting_substring_match(self):
        # "hello there" is not a dictionary key, but should still match
        # because "hello" is contained within it.
        self.assertEqual(self.bot.match_intent("hello there"), "greeting")

    def test_unknown_input_returns_none(self):
        self.assertIsNone(self.bot.match_intent("asdkjaslkdj"))

    def test_farewell_match(self):
        self.assertEqual(self.bot.match_intent("goodbye friend"), "farewell")


class TestGetResponse(unittest.TestCase):
    def setUp(self):
        self.bot = RuleBasedChatbot(bot_name="TestBot")

    def test_known_input_returns_a_configured_response(self):
        response = self.bot.get_response("hi")
        possible = self.bot.knowledge_base["greeting"]["responses"]
        self.assertIn(response, possible)

    def test_unknown_input_returns_a_fallback(self):
        response = self.bot.get_response("qwertyuiop")
        self.assertIn(response, self.bot.fallback_responses)

    def test_conversation_is_logged(self):
        self.bot.get_response("hello")
        self.assertEqual(len(self.bot.conversation_log), 1)
        self.assertEqual(self.bot.conversation_log[0][0], "hello")


class TestExitDetection(unittest.TestCase):
    def setUp(self):
        self.bot = RuleBasedChatbot()

    def test_exit_command_detected(self):
        self.assertTrue(self.bot.should_exit("exit"))
        self.assertTrue(self.bot.should_exit("bye"))
        self.assertTrue(self.bot.should_exit("quit"))

    def test_non_exit_command_not_detected(self):
        self.assertFalse(self.bot.should_exit("hello"))


if __name__ == "__main__":
    unittest.main()
