"""
FoxPi Core Algorithms — High-precision π computation.
Implements exact integer-scaled implementations of historical and elite formulas.
"""

from typing import Generator, Tuple

def get_ramanujan_pi_terms(precision: int) -> Generator[Tuple[int, int, int], None, None]:
    """
    Ramanujan's legendary 1914 hypergeometric series for 1/π.
    Formula:
      1/π = (2√2 / 9801) * Σ [ (4k)! * (1103 + 26390k) / ((k!)^4 * 396^(4k)) ]
      
    Yields:
        Tuple[int, int, int]: (term_index, current_pi_estimate, current_term_value)
    """
    # Guard digits to mitigate rounding accumulation
    guard = 20
    scale = 10 ** (precision + guard)
    
    # Pre-calculate integer-scaled square root of 2: isqrt(2 * scale^2)
    # 2√2 * scale = isqrt(8 * scale^2)
    two_sqrt_two = isqrt(8 * (scale ** 2))
    
    total_sum = 0
    
    # Iterative hypergeometric factors
    # Holds: (4k)! / ((k!)^4 * 396^(4k))
    num_ratio = 1
    den_ratio = 1
    
    k = 0
    while True:
        # Linear term: (1103 + 26390k)
        linear = 1103 + 26390 * k
        
        # Current hypergeometric term
        term = (scale * num_ratio * linear) // den_ratio
        
        if term == 0:
            break
            
        total_sum += term
        
        # 1/pi = (2sqrt2/9801) * Sigma  =>  pi = 9801*scale^3 / (two_sqrt_two * total_sum)
        # (two_sqrt_two and total_sum each already carry one factor of scale)
        current_pi = (9801 * scale * scale * scale) // (two_sqrt_two * total_sum)
        final_pi = current_pi // (10 ** guard)
        
        yield k, final_pi, term
        
        # Hypergeometric updates for k -> k + 1 step
        # Multiplier derivation: (4k+1)(4k+2)(4k+3)(4k+4) / ((k+1)^4 * 396^4)
        num_ratio *= (4 * k + 1) * (4 * k + 2) * (4 * k + 3) * (4 * k + 4)
        den_ratio *= ((k + 1) ** 4) * 24591257856  # 396^4 = 24591257856
        k += 1


def get_chudnovsky_pi_terms(precision: int = 100) -> Generator[Tuple[int, int, int], None, None]:
    """
    Chudnovsky series computed one term at a time for convergence
    visualization (the `explore` command). Recomputes binary splitting
    from scratch each step — O(k^2) overall, which is fine for the
    handful of terms `explore` requests. Use compute_chudnovsky_pi for
    actual high-precision computation.

    Yields:
        Tuple[int, int, int]: (term_index, current_pi_estimate, term_magnitude)
    """
    guard = 20
    scale = 10 ** (precision + guard)
    C = 640320
    C3_OVER_24 = (C ** 3) // 24

    def bs(a: int, b: int) -> Tuple[int, int, int]:
        if b - a == 1:
            if a == 0:
                P = 1
                Q = 1
            else:
                P = (6 * a - 5) * (2 * a - 1) * (6 * a - 1)
                Q = (a ** 3) * C3_OVER_24
            T = P * (13591409 + 545140134 * a)
            if a % 2 == 1:
                T = -T
            return P, Q, T
        else:
            m = (a + b) // 2
            P1, Q1, T1 = bs(a, m)
            P2, Q2, T2 = bs(m, b)
            return P1 * P2, Q1 * Q2, Q2 * T1 + P1 * T2

    sqrt_10005 = isqrt(10005 * (scale ** 2))
    max_terms = (precision // 14) + 2  # Chudnovsky gives ~14 digits/term

    k = 1
    while k <= max_terms:
        _, _, single_T = bs(k - 1, k)
        term_magnitude = abs(single_T) if single_T != 0 else 1

        _, Q, T = bs(0, k)
        numerator = 426880 * sqrt_10005 * Q
        pi_val = numerator // T
        final_pi = pi_val // (10 ** guard)

        yield k - 1, final_pi, term_magnitude
        k += 1


def compute_chudnovsky_pi(precision: int) -> int:
    """
    The Chudnovsky algorithm utilizing Binary Splitting execution logic.
    Provides ~14 digits per iteration. Used by world-record engines.
    """
    guard = 20
    scale = 10 ** (precision + guard)
    
    # Constants
    C = 640320
    C3_OVER_24 = (C ** 3) // 24
    
    # Binary splitting helper to divide-and-conquer huge integer expansions
    def bs(a: int, b: int) -> Tuple[int, int, int]:
        if b - a == 1:
            if a == 0:
                P = 1
                Q = 1
            else:
                P = (6 * a - 5) * (2 * a - 1) * (6 * a - 1)
                Q = (a ** 3) * C3_OVER_24
            T = P * (13591409 + 545140134 * a)
            if a % 2 == 1:
                T = -T
            return P, Q, T
        else:
            m = (a + b) // 2
            P1, Q1, T1 = bs(a, m)
            P2, Q2, T2 = bs(m, b)
            P = P1 * P2
            Q = Q1 * Q2
            T = Q2 * T1 + P1 * T2
            return P, Q, T

    # Estimate required terms: ~14 digits per term
    terms = (precision // 14) + 1
    P, Q, T = bs(0, terms)
    
    # 426880 * √10005
    sqrt_10005 = isqrt(10005 * (scale ** 2))
    numerator = 426880 * sqrt_10005 * Q
    
    pi = numerator // T
    return pi // (10 ** guard)


def compute_machin_pi(precision: int) -> int:
    """Classical Machin formula with scaled integer arithmetic."""
    guard = 20
    scale = 10 ** (precision + guard)
    
    def arccot(x: int, base_scale: int) -> int:
        total = base_scale // x
        term = total
        n = 3
        x2 = x * x
        sign = -1
        while True:
            term = term // x2
            if term == 0:
                break
            total += sign * (term // n)
            sign = -sign
            n += 2
        return total
        
    pi_approx = 4 * (4 * arccot(5, scale) - arccot(239, scale))
    return pi_approx // (10 ** guard)


def generate_bbp_spigot(digit_position: int) -> Generator[str, None, None]:
    """
    Bailey-Borwein-Plouffe (BBP) Spigot implementation.
    Extracts hexadecimal digits of π starting directly at 'digit_position'.
    Does not require calculating any preceding digits.
    """
    from decimal import Decimal, getcontext

    # Native float (53-bit mantissa) loses precision after ~13-14 hex digits
    # of summation at deeper positions, corrupting trailing output digits.
    # Use Decimal with enough guard digits to keep all 16 requested digits exact.
    getcontext().prec = max(30, len(str(digit_position)) + 30)

    def series_sum(n: int, j: int) -> Decimal:
        s = Decimal(0)
        for k in range(n + 1):
            r = 8 * k + j
            s = (s + Decimal(pow(16, n - k, r)) / r) % 1
        k = n + 1
        while True:
            term = Decimal(16) ** (n - k) / (8 * k + j)
            if term < Decimal("1e-30"):
                break
            s += term
            k += 1
        return s

    n = digit_position - 1
    s1 = series_sum(n, 1)
    s2 = series_sum(n, 4)
    s3 = series_sum(n, 5)
    s4 = series_sum(n, 6)

    pid = (4 * s1 - 2 * s2 - s3 - s4) % 1
    if pid < 0:
        pid += 1

    for _ in range(16):
        pid *= 16
        digit = int(pid)
        yield hex(digit)[2:].upper()
        pid -= digit


def isqrt(n: int) -> int:
    """High-performance standard Newton-Raphson integer square root engine."""
    if n < 0:
        raise ValueError("Square root of a negative integer is undefined.")
    if n == 0:
        return 0
    x = 2 ** ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y
