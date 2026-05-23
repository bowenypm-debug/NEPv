# Project Report: Numerical Analysis of Nonlinear Eigenvalue Problems (NEPv)

---

## Problem Statement

Traditional linear eigenvalue problems seek a scalar lambda and a non-zero vector v such that Av = \(\lambda \)* v, where the matrix A is constant. However, in many real-world systems—such as electronic structure calculations in quantum chemistry (e.g., Self-Consistent Field equations) and advanced machine learning data clustering—the matrix itself changes depending on its own eigenvectors. This is a Nonlinear Eigenvalue Problem with Eigenvector Dependency (NEPv), mathematically stated as:

A(v)v = lambda * v

Because the operator A(v) changes dynamically with the state vector v, traditional direct linear algebra methods (like standard QR algorithms) cannot solve it directly. The system requires iterative numerical solvers. This project implements a computational simulator to analyze the convergence behaviors, stability boundaries, and common failure states of these solvers within a controlled two-dimensional (2x2) coordinate matrix landscape.

---

## Methodology

The platform implements a comparative framework between two foundational numerical strategies used to resolve the self-consistency loop:

### 1. Self-Consistent Field (SCF) Iteration
The SCF method treats the problem as a sequence of standard linear eigenvalue problems. It fixes the current vector state v_k to build a static matrix snapshot, solves the resulting linear problem, and updates the vector for the next step:
*   Step Implementation: Given an initial guess v_0, the algorithm builds the temporary matrix A(v_k).
*   Linear Solver Phase: It computes the standard eigenvalues and eigenvectors of A(v_k).
*   Update: The eigenvector corresponding to the targeted algebraic property is chosen as v_{k+1}, normalized such that its length equals 1, and the loop repeats until compliance criteria are met.

### 2. Newton-Based Error Minimization Method
Rather than solving a sequence of linear problems, the Newton-based approach re-frames the NEPv as finding the roots of a continuous algebraic error vector function F(v).
*   Step Implementation: The system sets up the residual algebraic function representing the system error variance.
*   Descent Step: It utilizes numerical approximations of the system's local sensitivities to calculate a correction trajectory vector.
*   Damping Parameter: To maintain local stability without complex line-search algorithms, a fixed stabilization step size (damping factor) of 0.4 is applied to update the vector path at each step.

---

## Evaluation Methods & Dataset

### Evaluation Methods
The algorithms are evaluated dynamically based on two core criteria:
1.  Geometric Trajectory mapping: Tracking the step-by-step spatial coordinates of v_k projected onto a dashed Unit Circle Boundary to observe geometric convergence paths.
2.  Convergence Rate Analysis: Monitoring how quickly the residual system error approaches zero within a strict computational budget ceiling of 15 iterations.

### Evaluation Dataset (Custom Parameter Environment)
Because NEPv behavior depends entirely on the formulation of the nonlinearity, the software generates a real-time synthetic environment driven by user-controlled variables. The dynamic matrix template is configured as:
*   A base symmetric linear matrix kernel.
*   Two independent nonlinearity scaling weights (alpha and beta) that control how aggressively the state vector v twists and scales the matrix operator A(v) during runtime loops.

---

## Experimental Results

Through running simulations across varying degrees of nonlinearity weights (alpha, beta), two distinct behavioral archetypes were recorded:

1.  Low-Nonlinearity Convergence Success: When scaling parameters are low, both the SCF and Newton methods successfully navigate to the exact same stable eigenvector destination on the unit circle. The Newton method tracks a direct algebraic error minimization descent path, while the SCF method approaches the solution through geometric coordinate shifts.
2.  High-Nonlinearity Algorithmic Pitfalls: Pushing nonlinearity weights beyond critical system thresholds consistently triggers two classic numerical failure modes:
    *   SCF Infinite Oscillation: The SCF loop falls into an infinite back-and-forth bounce pattern. Because it applies full corrections without damping, the algorithm overcorrects past the stable solution point every single step, bouncing endlessly between two distinct state coordinates until hitting the 15-iteration cap.
    *   Newton Iteration Exhaustion: When initialized far from the stable root coordinate, the rigid 0.4 step size prevents the Newton method from closing the distance quickly enough, leading to execution termination before convergence is reached.

---

##  AI Collaboration & Verification Statement

This project was built with assistance from AI (Gemini in particular) to fact check if everything said in the website is correct, to polish application UI and helped in debugging.

### What the AI Assisted With:
* Structuring the interactive web framework and page navigation mechanics via Streamlit.
* Refining copy across all three pages to eliminate dense academic jargon and simplify explanations of the "self-consistency loop."
* Assisting with the formatting and compilation of this README documentation.

### What Was Independently Verified By Hand & Code:
* **Mathematical Core:** The custom algebraic setups, matrix definitions, and $2 \times 2$ nonlinear equations were structured and calculated manually before deployment.
* **Solver Algorithm Validation:** The implementation logic for the Self-Consistent Field loop and the Newton based method was written and tested step-by-step using a script to ensure the Scipy/Numpy calculations lined up exactly with the calculations done by hand.
* **Trajectory & Error Testing:** The specific threshold boundary limits (such as the 15-iteration cutoff limit and the vector orientation dot product verification layer) were intentionally code-tested to accurately model and simulate structural pitfalls without application crashing.

---

## References
* Werner, T. (2025). An inexact Matrix-Newton method for solving NEPv. *Linear Algebra and its Applications*, 721, 1-25. https://doi.org/10.1016/j.laa.2024.11.003
* Streamlit. (n.d.). *Streamlit cheat sheet*. Retrieved May 20, 2026, from https://docs.streamlit.io/develop/quick-reference/cheat-sheet
