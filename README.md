#  Interactive NEPv Learning Suite & Solver

An interactive 3-page web application built with Streamlit to demonstrate the mechanics, geometry, and algorithms used to solve Nonlinear Eigenvalue Problems with Eigenvector Dependency (NEPv). 

This platform allows users to manipulate nonlinear matrix parameters in a 2x2 coordinate system and visually map out the convergence paths of two classic numerical solvers: Self-Consistent Field (SCF) Iteration and a Newton-Based Method.

---

##  Getting Started & Installation

### 1. Clone the Repository
Open your terminal and run the following commands:
git clone https://github.com/bowenypm-debug/NEPv
cd NEPv

### 2. Install Dependencies
Make sure you have Python installed, then install the required mathematical and web-framework libraries using pip:
pip install streamlit numpy scipy matplotlib

### 3. Run the App Locally
Launch the application using Streamlit:
streamlit run Introduction.py

---

##  Design Choices & App Flow

To prevent textbook fatigue and build genuine student intuition, the application is divided into a clear, 3-page narrative arc:

1. Page 1: Introduction (Introduction.py)
   * The 3 Levels: Steps the user sequentially from Level 1 (Traditional linear systems), to Level 2 (Nonlinear only in the scalar parameter lambda), and finally to Level 3 (Nonlinear in the vector state v).
   * The Loop Concept: Explains "self-consistency" not through dry proofs, but as a clear, 3-step continuous feedback loop.

2. Page 2: Solvers & Calculators (pages/1_Examples_and_Solvers.py)
   * Dual Algorithms: Contrasts the algorithmic behavior of the Self-Consistent Field (SCF) method (solving a loop of traditional linear problems) against a Newton-Based Method (minimizing an algebraic error vector using a 0.4 step size).
   * Visual Trajectory Canvas: Uses matplotlib to project the 2x2 eigenvectors directly onto a dashed Unit Circle Boundary so users can watch the paths converge or fail in real time.
   * Custom Parameter Playground: Exposes base matrix variables and custom nonlinearity sliders (alpha, beta) so users can experiment with different mathematical environments.

3. Page 3: Applications & Pitfalls (pages/2_Applications_and_Pitfalls.py)
   * Real-World Uses: Explains how NEPv solves real problems in Quantum Chemistry (finding electron clouds) and Machine Learning (clustering complex data) without dense academic jargon.
   * Algorithmic Pitfalls: Intuitively connects failure states back to the math (SCF getting stuck in infinite oscillations due to overcorrection, and Newton methods taking too many iterations due to initial guess distance).

---

##  Limitations

This software application is built strictly as a visual learning environment. Take note of the following limitations:

* Fixed Dimensions (2x2 Matrix Only): The underlying linear algebra formulas, code, and graphing functions are hardcoded for two-dimensional coordinate transformations. It cannot process larger matrices.
* Fixed Newton Step Size (0.4): The Newton-based method utilizes a rigid, non-adaptive step size of 0.4. It lacks an advanced line-search fallback to alter its travel path automatically.
* Vector Sign Flipping Constraint: Because standard eigenvalue solvers can output equivalent solutions pointing 180 degrees apart, the trajectory loop uses a dot product layer to keep direction orientation consistency on the graph.
* Iteration Cap (15 Steps): The solver loops terminate automatically at 15 iterations. Pushing nonlinearity weights too high will reliably trigger the "Infinite Oscillation" pitfall for the SCF method.

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
