"""
End-to-end tests for cli.py, run as a subprocess to match real usage.
"""
import subprocess
import sys
import os
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLI = os.path.join(ROOT, "cli.py")


def run(*args):
    result = subprocess.run(
        [sys.executable, CLI, *args],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
    )
    return result.returncode, result.stdout, result.stderr


class TestValidation(unittest.TestCase):
    def test_negative_digit_count_rejected(self):
        code, out, err = run("digits", "-5", "--method", "chudnovsky")
        self.assertEqual(code, 1)
        self.assertIn("Error", err)

    def test_negative_bbp_position_rejected(self):
        code, out, err = run("bbp", "-10")
        self.assertEqual(code, 1)
        self.assertIn("Error", err)

    def test_zero_bbp_position_rejected(self):
        code, out, err = run("bbp", "0")
        self.assertEqual(code, 1)

    def test_zero_explore_terms_rejected(self):
        code, out, err = run("explore", "--terms", "0")
        self.assertEqual(code, 1)

    def test_missing_subcommand_errors(self):
        code, out, err = run()
        self.assertNotEqual(code, 0)


class TestNormalUsage(unittest.TestCase):
    def test_digits_chudnovsky(self):
        code, out, err = run("digits", "20", "--method", "chudnovsky")
        self.assertEqual(code, 0)
        self.assertIn("3.14159265358979323846", out)

    def test_digits_large_count_no_crash(self):
        # Regression check for the sys.set_int_max_str_digits fix.
        code, out, err = run("digits", "5000", "--method", "chudnovsky")
        self.assertEqual(code, 0)
        self.assertIn("3.14159265358979323846", out)

    def test_bbp(self):
        code, out, err = run("bbp", "100")
        self.assertEqual(code, 0)
        self.assertIn("C29B7C97C50DD3F8", out)

    def test_explore_chudnovsky_runs(self):
        code, out, err = run("explore", "--method", "chudnovsky", "--terms", "5")
        self.assertEqual(code, 0)

    def test_explore_delivers_requested_term_count(self):
        # Regression check: explore's internal generator precision used to
        # be hardcoded to 100, which caps Chudnovsky at 9 terms and
        # Ramanujan at 16 -- so the *default* `explore` (--terms 30) always
        # silently fell short of its own default term count. Precision now
        # scales with --terms, so both methods should deliver the full
        # count requested, well past the old hardcoded caps.
        for method, terms in [("ramanujan", 30), ("chudnovsky", 30), ("chudnovsky", 50)]:
            code, out, err = run("explore", "--method", method, "--terms", str(terms))
            self.assertEqual(code, 0)
            self.assertNotIn("series exhausted", out,
                              f"{method} with --terms {terms} exhausted early")
            term_rows = sum(1 for line in out.splitlines() if line[:1].isdigit())
            self.assertEqual(term_rows, terms,
                              f"{method} with --terms {terms} only produced {term_rows} rows")

    def test_compare_runs(self):
        code, out, err = run("compare")
        self.assertEqual(code, 0)
        self.assertIn("Chudnovsky", out)
        self.assertIn("Machin", out)


if __name__ == "__main__":
    unittest.main()
