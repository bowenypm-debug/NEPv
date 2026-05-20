import streamlit as st

st.set_page_config(page_title="NEPv Academy", layout="wide")

st.title("🧩 Introduction to Nonlinear Eigenvalue Problems (NEPv)")

st.markdown("""
### What is an NEPv?
In a traditional eigenvalue problem, you are given a fixed matrix $A$ and you look for a scaling factor $\lambda$ and vector $v$ such that:
$$Av = \lambda v$$

In an **NEPv**, the matrix itself is **dependent on the vector**. The terrain changes as you walk on it:
$$A(v)v = \lambda v$$

### 🌌 Where is this used in the real world?
1. **Quantum Chemistry (DFT):** When simulating molecules, the location of electrons creates an electric field. That electric field changes the matrix that determines where the electrons want to go!
2. **Bose-Einstein Condensates:** In physics, clumps of ultra-cold atoms interact with each other, altering the quantum potential well they sit in.

### ⚠️ The Dangerous Pitfalls of Nonlinearity
Because the problem is nonlinear, mathematical guarantees break down:
* **Multiple Solutions:** A single system can have many more valid eigenvector states than its dimensions suggest.
* **Chaos & Limit Cycles:** Standard algorithm loops can get trapped bouncing back and forth between two states forever, never finding a solution.
""")

st.info("👈 Use the sidebar navigation to move to Page 2 and visualize this live!")