"""
Tests for core/algorithms.py, checked against reference digits of pi
computed independently (mpmath, 250 decimal digits of working precision)
rather than against this codebase's own prior output.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.algorithms import (
    get_ramanujan_pi_terms,
    get_chudnovsky_pi_terms,
    compute_chudnovsky_pi,
    compute_machin_pi,
    generate_bbp_spigot,
    isqrt,
)

# Reference decimal digits of pi, "3" + 194 fractional digits (mpmath, dps=250).
PI_DECIMAL = (
    "314159265358979323846264338327950288419716939937510582097494459230781640628620899862803"
    "4825342117067982148086513282306647093844609550582231725359408128481117450284102701938521"
    "1055596446229489549303819644288"
)

# Reference hex digits of pi's fractional part, position 1 = first digit after the point.
PI_HEX = (
    "243F6A8885A308D313198A2E03707344A4093822299F31D0082EFA98EC4E6C89452821E638D01377BE5466CF3"
    "4E90C6CC0AC29B7C97C50DD3F84D5B5"
)


class TestIsqrt(unittest.TestCase):
    def test_perfect_squares(self):
        for n in [0, 1, 4, 9, 100, 10 ** 20]:
            self.assertEqual(isqrt(n) ** 2, n)

    def test_non_perfect_squares_floor(self):
        for n in [2, 3, 5, 10, 99, 10 ** 20 + 1]:
            root = isqrt(n)
            self.assertLessEqual(root * root, n)
            self.assertGreater((root + 1) ** 2, n)

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            isqrt(-1)


class TestChudnovsky(unittest.TestCase):
    def test_matches_reference(self):
        for precision in [1, 10, 50, 100, 194]:
            got = str(compute_chudnovsky_pi(precision))
            self.assertEqual(got, PI_DECIMAL[:precision + 1],
                              f"mismatch at precision={precision}")

    def test_zero_precision_does_not_crash(self):
        got = str(compute_chudnovsky_pi(0))
        self.assertEqual(got, "3")


class TestRamanujan(unittest.TestCase):
    def test_matches_reference(self):
        for precision in [10, 50, 100]:
            last = None
            for term in get_ramanujan_pi_terms(precision):
                last = term
            got = str(last[1])
            self.assertEqual(got, PI_DECIMAL[:precision + 1],
                              f"mismatch at precision={precision}")

    def test_terminates(self):
        # Regression check: this used to be an infinite/near-infinite
        # generator before the factor-of-8 formula fix.
        count = sum(1 for _ in get_ramanujan_pi_terms(50))
        self.assertGreater(count, 0)
        self.assertLess(count, 100)


class TestChudnovskyTerms(unittest.TestCase):
    def test_converges_to_reference(self):
        last = None
        for term in get_chudnovsky_pi_terms(50):
            last = term
        got = str(last[1])
        self.assertEqual(got[:15], PI_DECIMAL[:15])

    def test_terminates(self):
        count = sum(1 for _ in get_chudnovsky_pi_terms(50))
        self.assertGreater(count, 0)
        self.assertLess(count, 50)


class TestMachin(unittest.TestCase):
    def test_matches_reference(self):
        for precision in [10, 50, 100]:
            got = str(compute_machin_pi(precision))
            self.assertEqual(got, PI_DECIMAL[:precision + 1],
                              f"mismatch at precision={precision}")


class TestBBP(unittest.TestCase):
    def test_matches_reference_at_various_positions(self):
        for pos in [1, 25, 50, 100]:
            got = "".join(generate_bbp_spigot(pos))
            expected = PI_HEX[pos - 1:pos - 1 + 16]
            self.assertEqual(got, expected, f"mismatch at position={pos}")

    def test_position_one_starts_series(self):
        got = "".join(generate_bbp_spigot(1))
        self.assertEqual(got, PI_HEX[:16])


if __name__ == "__main__":
    unittest.main()
