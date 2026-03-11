# We'll compare convergence of several π series:
# - Leibniz (Gregory-Leibniz)
# - Nilakantha
# - Ramanujan (1914) 1/π series
# - Chudnovsky (Ramanujan-type) 1/π series
#
# We'll compute a high-precision reference π using Chudnovsky with several terms,
# then tabulate the error for each method with a small number of terms.

from decimal import Decimal, getcontext
import math
import pandas as pd

# High precision for reference
getcontext().prec = 200

def chudnovsky_pi(k_terms=6):
    # 1/pi = (12 / 640320^(3/2)) * sum_k (-1)^k * (6k)! * (13591409 + 545140134k) / ((3k)! (k!)^3 * 640320^(3k))
    C = Decimal(640320)
    C3_2 = (C**3).sqrt()  # 640320^(3/2)
    prefactor = Decimal(12) / C3_2
    S = Decimal(0)
    for k in range(k_terms):
        sixk_fact = Decimal(math.factorial(6*k))
        threek_fact = Decimal(math.factorial(3*k))
        k_fact_cubed = Decimal(math.factorial(k))**3
        num = sixk_fact * Decimal(13591409 + 545140134*k) * (Decimal(-1) ** k)
        den = threek_fact * k_fact_cubed * (C ** (3*k))
        S += num / den
    inv_pi = prefactor * S
    return Decimal(1) / inv_pi

# Reference π with high precision
pi_ref = chudnovsky_pi(k_terms=8)

# Utilities
def count_matching_digits(x: Decimal, y: Decimal, max_digits=50):
    # Count matching digits from the start (including leading "3.") until a mismatch occurs
    sx = f"{x:.{max_digits}f}"
    sy = f"{y:.{max_digits}f}"
    # Ensure same length
    n = min(len(sx), len(sy))
    count = 0
    for i in range(n):
        if sx[i] == sy[i]:
            if sx[i].isdigit():
                count += 1
        else:
            break
    return count

def leibniz_pi(n_terms):
    # π = 4 * sum_{n=0}^{N} (-1)^n/(2n+1)
    s = Decimal(0)
    one = Decimal(1)
    for n in range(n_terms+1):
        term = one / Decimal(2*n+1)
        if n % 2 == 0:
            s += term
        else:
            s -= term
    return Decimal(4) * s

def nilakantha_pi(n_terms):
    # π = 3 + sum_{n=1}^{N} (-1)^{n-1} * 4 / ((2n)*(2n+1)*(2n+2))
    s = Decimal(3)
    for n in range(1, n_terms+1):
        term = Decimal(4) / (Decimal(2*n) * Decimal(2*n+1) * Decimal(2*n+2))
        if (n-1) % 2 == 0:
            s += term
        else:
            s -= term
    return s

def ramanujan_pi(k_terms):
    # 1/π = (2√2 / 9801) * sum_{k=0}∞ (4k)! (1103 + 26390k) / ((k!)^4 * 396^(4k))
    two = Decimal(2)
    sqrt2 = two.sqrt()
    prefactor = (two*sqrt2) / Decimal(9801)
    S = Decimal(0)
    for k in range(k_terms):
        fourk_fact = Decimal(math.factorial(4*k))
        k_fact_4 = Decimal(math.factorial(k))**4
        num = fourk_fact * Decimal(1103 + 26390*k)
        den = k_fact_4 * (Decimal(396) ** (4*k))
        S += num / den
    inv_pi = prefactor * S
    return Decimal(1) / inv_pi

# Build comparison table
rows = []

# Leibniz: try 10, 100, 1000, 10000 terms
for N in [10, 100, 1000, 10000]:
    getcontext().prec = 200
    approx = leibniz_pi(N)
    err = abs(approx - pi_ref)
    digits = count_matching_digits(approx, pi_ref, max_digits=60)
    rows.append({"Method": "Leibniz", "Terms": N, "Approx π": f"{approx:.12f}", "Abs Error": f"{err:.2E}", "Matching Digits": digits})

# Nilakantha: similar N
for N in [10, 100, 1000, 10000]:
    getcontext().prec = 200
    approx = nilakantha_pi(N)
    err = abs(approx - pi_ref)
    digits = count_matching_digits(approx, pi_ref, max_digits=60)
    rows.append({"Method": "Nilakantha", "Terms": N, "Approx π": f"{approx:.12f}", "Abs Error": f"{err:.2E}", "Matching Digits": digits})

# Ramanujan: 1..3 terms
for k in [1, 2, 3]:
    getcontext().prec = 200
    approx = ramanujan_pi(k)
    err = abs(approx - pi_ref)
    digits = count_matching_digits(approx, pi_ref, max_digits=60)
    rows.append({"Method": "Ramanujan 1/π", "Terms": k, "Approx π": f"{approx:.12f}", "Abs Error": f"{err:.2E}", "Matching Digits": digits})

# Chudnovsky: 1..3 terms
for k in [1, 2, 3]:
    getcontext().prec = 200
    approx = chudnovsky_pi(k)
    err = abs(approx - pi_ref)
    digits = count_matching_digits(approx, pi_ref, max_digits=60)
    rows.append({"Method": "Chudnovsky 1/π", "Terms": k, "Approx π": f"{approx:.12f}", "Abs Error": f"{err:.2E}", "Matching Digits": digits})

df = pd.DataFrame(rows)
print(df)
