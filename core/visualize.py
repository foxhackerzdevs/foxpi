"""
FoxPi Visualization Module
Handles high-fidelity CLI output formats.
"""

import time
from typing import List, Dict, Any

def render_convergence_table(history: List[Dict[str, Any]]) -> None:
    """Prints a beautiful live convergence log to stdout."""
    print(f"\n{'Iteration':<12} | {'Term Delta (Log10)':<20} | {'Pi Preview (First 15 Digits)':<20}")
    print("-" * 60)
    for entry in history:
        idx = entry['step']
        delta_len = len(str(entry['delta']))
        pi_str = str(entry['pi'])
        pi_preview = f"{pi_str[0]}.{pi_str[1:15]}..." if len(pi_str) > 15 else pi_str
        print(f"{idx:<12} | -10^{delta_len:<16} | {pi_preview:<20}")

def render_comparison(results: List[Dict[str, Any]]) -> None:
    """Displays benchmark metrics comparing different numerical formulas."""
    print(f"\n{'Algorithm':<15} | {'Precision (Digits)':<20} | {'Time Elapsed (s)':<18}")
    print("-" * 60)
    for res in results:
        print(f"{res['algo']:<15} | {res['precision']:<20} | {res['time']:.6f}s")
