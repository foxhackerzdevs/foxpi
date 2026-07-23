# cli.py
#!/usr/bin/env python3
"""
FoxPi — High-precision π & mathematical explorer
"""

import sys
import time
import argparse
from pathlib import Path
from typing import List

from core.algorithms import (
    get_ramanujan_pi_terms,
    get_chudnovsky_pi_terms,
    compute_chudnovsky_pi,
    compute_machin_pi,
    generate_bbp_spigot,
    isqrt,
)
from core.visualize import render_convergence_table, render_comparison

def main():
    parser = argparse.ArgumentParser(prog="foxpi", description="High-precision π explorer 🦊")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # digits command
    d = sub.add_parser("digits", help="Compute N digits of π")
    d.add_argument("count", type=int, help="Number of decimal digits")
    d.add_argument("--method", choices=["ramanujan", "chudnovsky", "machin"], default="chudnovsky")

    # explore command
    e = sub.add_parser("explore", help="Live convergence visualisation")
    e.add_argument("--method", choices=["ramanujan", "chudnovsky"], default="ramanujan")
    e.add_argument("--terms", type=int, default=30)

    # compare command
    sub.add_parser("compare", help="Benchmark multiple algorithms")

    # bbp spigot
    b = sub.add_parser("bbp", help="Extract hexadecimal digits using BBP formula")
    b.add_argument("position", type=int, default=1, help="Starting digit position (1 = first after decimal)")

    args = parser.parse_args()

    if args.cmd == "digits" and args.count < 0:
        print(f"Error: digit count must be >= 0 (got {args.count}).", file=sys.stderr)
        sys.exit(1)
    if args.cmd == "bbp" and args.position < 1:
        print(f"Error: position must be >= 1 (got {args.position}); 1 is the first hex digit after the point.", file=sys.stderr)
        sys.exit(1)
    if args.cmd == "explore" and args.terms < 1:
        print(f"Error: --terms must be >= 1 (got {args.terms}).", file=sys.stderr)
        sys.exit(1)

    if args.cmd == "digits":
        # Python 3.11+ caps int->str conversion at 4300 digits by default;
        # raise it to fit the requested precision (plus a small margin).
        sys.set_int_max_str_digits(max(4300, args.count + 20))

        start = time.perf_counter()
        if args.method == "chudnovsky":
            pi_int = compute_chudnovsky_pi(args.count)
        elif args.method == "ramanujan":
            # Take last term
            last = None
            for term in get_ramanujan_pi_terms(args.count):
                last = term
            pi_int = last[1]
        else:  # machin
            pi_int = compute_machin_pi(args.count)

        elapsed = time.perf_counter() - start
        pi_str = str(pi_int)
        print(f"\nπ ({args.count} digits) using {args.method.capitalize()}:")
        print(f"{pi_str[0]}.{pi_str[1:]}")
        print(f"Time: {elapsed:.4f}s")

    elif args.cmd == "explore":
        print(f"Exploring convergence with {args.method}...\n")
        history = []
        gen = get_ramanujan_pi_terms(100) if args.method == "ramanujan" else get_chudnovsky_pi_terms(100)

        for i in range(args.terms):
            try:
                k, pi_est, delta = next(gen)
                history.append({'step': k, 'pi': pi_est, 'delta': delta})
                pi_s = str(pi_est)
                print(f"Term {k:3d} → π ≈ {pi_s[0]}.{pi_s[1:15]}...", end="\r")
            except StopIteration:
                print(f"\n(series exhausted at {len(history)} term(s) for this precision — "
                      f"further terms would add no more distinguishable digits)")
                break
        print("\n")
        render_convergence_table(history)

    elif args.cmd == "compare":
        print("Benchmarking algorithms...\n")
        results = []
        for method, func in [("Chudnovsky", lambda: compute_chudnovsky_pi(1000)),
                             ("Machin", lambda: compute_machin_pi(1000))]:
            t0 = time.perf_counter()
            func()
            t1 = time.perf_counter()
            results.append({'algo': method, 'precision': 1000, 'time': t1-t0})
        render_comparison(results)

    elif args.cmd == "bbp":
        print(f"Extracting 16 hex digits of π starting at position {args.position}:")
        digits = list(generate_bbp_spigot(args.position))
        print("".join(digits))
        print("(BBP Spigot — hexadecimal)")

if __name__ == "__main__":
    main()
