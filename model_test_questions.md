# AI Model Comparative Test
## Test both M2.7 and GLM-5 with the same prompts

---

## TEST 1: Capacitor Discharge (Physics)

**Question:**
A 100μF capacitor is charged to 12V, then discharges through a 1MΩ resistor.

Calculate:
1. Time constant τ
2. Voltage after 5 seconds
3. Time for voltage to drop to 1V

Show all your calculations with units.

**Expected Answers:**
- τ = RC = 100 × 10⁻⁶ × 10⁶ = 100 seconds
- V(5s) = 12 × e^(-5/100) = 12 × e^(-0.05) ≈ 11.46 V
- t = τ × ln(12/1) = 100 × 2.485 ≈ 248.5 seconds

---

## TEST 2: Photoelectric Effect (Physics)

**Question:**
Light of wavelength 400nm shines on a metal with work function 2.5 eV.

Calculate:
1. Energy of incident photons (in eV)
2. Maximum kinetic energy of emitted electrons
3. Will photoelectrons be emitted? Explain.

**Expected Answers:**
- E = hc/λ = (6.626×10⁻³⁴ × 3×10⁸)/(400×10⁻⁹) = 4.97×10⁻¹⁹ J = 3.11 eV
- KE_max = E - Φ = 3.11 - 2.5 = 0.61 eV
- YES, because photon energy (3.11 eV) > work function (2.5 eV)

---

## TEST 3: Numerical Integration (Code)

**Question:**
Write a complete Python program that:
1. Uses the trapezoidal rule with 1000 intervals to calculate ∫₀^π sin(x)dx
2. Uses Simpson's rule to calculate the same integral
3. Compares both results with the exact answer (2)
4. Prints all three values

Make sure the code runs without errors.

**Expected Output Format:**
```
Trapezoidal: 1.9999...
Simpson: 2.0000...
Exact: 2.0
Difference (trap): ~0.0001
```

---

## TEST 4: Data Analysis (Code)

**Question:**
Write a complete Python program that:
1. Generates 1000 random numbers from a normal distribution (μ=50, σ=10)
2. Calculates and prints: mean, median, standard deviation
3. Creates a histogram with the fitted normal curve overlaid
4. Saves the plot as 'histogram.png'

**Expected Values (approximately):**
- Mean: ~50
- Median: ~50
- Std Dev: ~10

---

## TEST 5: Differential Equation (Math)

**Question:**
Solve the differential equation:
```
d²y/dx² + 2dy/dx + y = 0
```
With initial conditions: y(0) = 1, y'(0) = 0

Show the characteristic equation, roots, and final solution.

**Expected Answer:**
- Characteristic: r² + 2r + 1 = 0
- Roots: r = -1 (double root)
- Solution: y(x) = (1 + x)e^(-x)

---

## TEST 6: Series Convergence (Math)

**Question:**
Determine whether the series converges or diverges. If it converges, find its sum.
```
Σ(n=1 to ∞) n² / (n³ + 1)
```

Prove your answer.

**Expected Answer:**
- Converges (by limit comparison with 1/n)
- Sum ≈ 0.5 (using integral test or computer)

---

## TEST 7: Floating Point (Concept)

**Question:**
In Python, run this code:
```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

Explain why you get these results. What is the underlying cause?

**Expected Explanation:**
- Output: 0.30000000000000004 and False
- Cause: IEEE 754 floating-point representation
- 0.1 and 0.2 cannot be represented exactly in binary
- Rounding errors accumulate

---

## TEST 8: Halting Problem (Concept)

**Question:**
Explain the Halting Problem in simple terms. Why does it prove that perfect software testing is impossible?

**Expected Answer:**
- Halting Problem: Given a program and input, determine if it halts
- Turing proved it's undecidable (1936)
- Proof by contradiction: Assume H exists, construct paradox
- Implication: No program can perfectly predict all other programs

---

## TEST 9: Complex Physics Problem

**Question:**
A satellite of mass 500kg orbits Earth at height 400km.
M_Earth = 5.97×10²⁴ kg, R_Earth = 6371 km, G = 6.674×10⁻¹¹

Calculate:
1. Orbital velocity
2. Orbital period
3. Total energy of the orbit
4. Write Python code to verify these calculations

**Expected Answers:**
- v ≈ 7.67 km/s
- T ≈ 92.6 minutes
- E ≈ -1.47×10¹⁰ J (negative = bound orbit)

---

## TEST 10: Matrix Operations (Code)

**Question:**
Write a complete Python program that:
1. Defines matrix A = [[3,1],[2,2]]
2. Calculates eigenvalues and eigenvectors
3. Calculates A¹⁰ numerically
4. Prints all results

Use numpy or implement manually.

**Expected:**
- Eigenvalues: λ₁ ≈ 4.414, λ₂ ≈ 0.586
- A¹⁰ ≈ [[2457, 1486], [2972, 1805]] (approximately)

---

## Scoring Sheet

| Test | Category | Max Score | M2.7 | GLM-5 |
|------|----------|-----------|-------|--------|
| 1 | Physics | 20 | | |
| 2 | Physics | 20 | | |
| 3 | Code | 20 | | |
| 4 | Code | 20 | | |
| 5 | Math | 20 | | |
| 6 | Math | 20 | | |
| 7 | Concept | 15 | | |
| 8 | Concept | 15 | | |
| 9 | Complex | 20 | | |
| 10 | Code | 20 | | |
| **TOTAL** | | **190** | | |

## Evaluation Criteria

**Physics (correct formulas, calculations, units):**
- 20: Perfect with clear working
- 15: Minor error, correct method
- 10: Partial solution, multiple errors
- 5: Major conceptual errors
- 0: No attempt or completely wrong

**Code (runs, correct output, good style):**
- 20: Runs perfectly, clean code
- 15: Runs with minor issues
- 10: Has bugs but shows understanding
- 5: Significant problems
- 0: Doesn't run or no attempt

**Math (proofs, derivations):**
- 20: Complete, rigorous proof
- 15: Mostly correct, minor gaps
- 10: Partial solution
- 5: Major errors
- 0: No attempt

**Concept (explanations):**
- 15: Clear, accurate explanation
- 10: Good but incomplete
- 5: Some understanding shown
- 0: No understanding
