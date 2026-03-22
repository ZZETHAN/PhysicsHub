# AI Model Capability Test Suite

## Test Categories

### 1. Physics Problem Solving (A-Level Physics)

**Test 1.1: Capacitor Discharge**
A 100μF capacitor is charged to 12V, then discharges through a 1MΩ resistor.
- Calculate the time constant
- Find the voltage after 5 seconds
- How long until voltage drops to 1V?

**Test 1.2: Electromagnetic Induction**
A coil with 200 turns, radius 5cm is placed in a magnetic field that increases from 0 to 0.5T in 0.1s.
- Calculate the emf induced
- If the coil has resistance of 10Ω, find the current

**Test 1.3: Photoelectric Effect**
Light of wavelength 400nm shines on a metal with work function 2.5eV.
- Calculate the maximum kinetic energy of emitted electrons
- Will photoelectrons be emitted?

### 2. Code Generation

**Test 2.1: Numerical Integration**
Write a Python program to calculate the integral of sin(x) from 0 to π using:
- Trapezoidal rule (1000 intervals)
- Simpson's rule
- Compare with exact answer

**Test 2.2: Data Analysis**
Generate 1000 random data points following a normal distribution (μ=50, σ=10). Calculate and visualize:
- Mean, median, standard deviation
- Histogram with fitted normal curve

**Test 2.3: Physics Simulation**
Simulate projectile motion with air resistance (F = -kv). Plot trajectory for different values of k.

### 3. Mathematical Reasoning

**Test 3.1: Differential Equations**
Solve: d²y/dx² + 2dy/dx + y = 0, y(0)=1, y'(0)=0

**Test 3.2: Matrix Operations**
For matrix A = [[3,1],[2,2]], find:
- Eigenvalues and eigenvectors
- A^10 (numerical)

**Test 3.3: Series Convergence**
Determine whether the series Σ(n=1 to ∞) n²/(n³+1) converges or diverges.

### 4. Complex Multi-Step Problem

**Test 4: Design Problem**
A satellite orbits Earth at height 400km. Design a mission to:
1. Calculate orbital velocity and period
2. Determine minimum Δv to transfer to a geostationary orbit (35786km)
3. Calculate fuel mass needed given specific impulse of 320s
4. Write a simulation to verify calculations

Assume: M_Earth = 5.97×10²⁴kg, R_Earth = 6371km, g₀ = 9.81m/s²

### 5. Edge Cases & Error Handling

**Test 5.1**: Explain why 0.1 + 0.2 ≠ 0.3 in floating point

**Test 5.2**: What happens when you divide by zero in different programming languages?

**Test 5.3**: Explain the halting problem in simple terms

---

## Scoring Rubric

| Category | Points | Criteria |
|----------|--------|----------|
| Physics Accuracy | /25 | Correct formulas, calculations, units |
| Code Correctness | /25 | Runs without error, produces correct output |
| Mathematical rigor | /20 | Proper derivations, clear reasoning |
| Problem solving | /15 | Breaks down complex problems correctly |
| Edge case handling | /15 | Explains limitations and edge cases |

**Total: /100**

---

## Expected Outputs for Each Test

### Test 1.1 (Capacitor Discharge)
- Time constant = RC = 100s
- V(5s) = 12 × e^(-0.05) ≈ 11.46V
- V = 1V at t = 460s

### Test 1.2 (EM Induction)
- emf = -N × dΦ/dt = -200 × (0.5 × π × 0.05²) / 0.1 ≈ -7.85V
- I = 0.785A

### Test 1.3 (Photoelectric Effect)
- E_photon = hc/λ = 4.97×10⁻¹⁹ J = 3.11eV
- KE_max = 3.11 - 2.5 = 0.61eV (Yes, electrons emitted)

### Test 3.1
- y(x) = (1+x)e^(-x)
