import unittest

from cogercita.agent import resolve_option


class AgentOptionResolutionTests(unittest.TestCase):
    def test_resolve_option_returns_exact_match_case_insensitive(self) -> None:
        result = resolve_option(["Presencial", "Telefónico"], "presencial")
        self.assertEqual(result.selected, "Presencial")
        self.assertEqual(result.alternatives, ["Telefónico"])

    def test_resolve_option_returns_alternatives_when_missing(self) -> None:
        result = resolve_option(["Madrid Centro", "Getafe"], "Leganés Butarque")
        self.assertIsNone(result.selected)
        self.assertEqual(result.alternatives, ["Madrid Centro", "Getafe"])


if __name__ == "__main__":
    unittest.main()
