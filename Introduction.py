import streamlit as st

st.set_page_config(page_title="NEPv Introduction", layout="wide")

st.title("🚀 An Introduction to Nonlinear Eigenvalue Problems (NEPv)")
st.markdown("---")

st.markdown(r"""
Welcome! This interactive web suite is designed to guide you through the theory, geometry, and computation of a fascinating frontier in advanced linear algebra: the **Nonlinear Eigenvalue Problem with respect to the eigenvector (NEPv)**.

To understand what an NEPv is and why it is unique, it helps to look at the topic in three distinct levels of mathematical complexity.
""")

# ---------------------------------------------------------
# The Three Levels of Eigenproblems
# ---------------------------------------------------------
st.markdown("## 🪜 The Three Levels of Eigenproblems")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Level 1: Traditional")
    st.info("**Linear Eigenproblem**")
    st.markdown(r"""
    In a standard linear algebra course, you work with a constant, rigid matrix $A$. You look for a scalar $\lambda$ and a non-zero vector $v$ such that:
    $$Av = \lambda v$$
    The matrix $A$ never changes; it acts as a fixed linear transformation on space.
    """)

with col2:
    st.markdown("### Level 2: NEP")
    st.warning("**Nonlinear in Parameter $\lambda$**")
    st.markdown(r"""
    In a standard Nonlinear Eigenvalue Problem (NEP), the matrix entries depend nonlinearly on the *eigenvalue* parameter itself, often written as $T(\lambda)$. 
    $$T(\lambda)v = 0$$
    This is frequently used in mechanical vibrations and structural engineering.
    """)

with col3:
    st.markdown("### Level 3: NEPv")
    st.success("**Nonlinear in Vector $v$**")
    st.markdown(r"""
    In an **NEPv**, the matrix entries depend directly on the state or coordinates of the *eigenvector* itself. 
    $$A(v)v = \lambda v$$
    As the vector $v$ changes position, the entire matrix landscape warps and mutates. This is our focus!
    """)

# ---------------------------------------------------------
# What is an NEPv & How do we solve it?
# ---------------------------------------------------------
st.markdown("---")
st.markdown(r"""
## ❓ What does an NEPv actually do?

In a traditional system, finding an eigenvector is like finding a fixed path on a permanent map. 

In an **NEPv**, it is like trying to find a path while your footsteps actively alter the terrain. Because the matrix $A(v)$ changes depending on $v$, computing a solution requires finding a state of **self-consistency**—a point where the vector creates a matrix landscape that, in turn, outputs that exact same vector direction back.

This framework is highly critical in advanced computational sciences, such as calculating electronic structures in quantum chemistry or solving data-clustering problems in machine learning.

---

## 🛠️ How do we solve an NEPv?

Because the matrix changes continuously as $v$ moves, we generally cannot use standard closed-form algebraic shortcuts (like finding $\det(A - \lambda I) = 0$). Instead, computers must rely on **iterative numerical methods** to hunt down stable solutions. 

On this website, you will explore two primary classes of solvers:

1. **Self-Consistent Field (SCF) Iteration:** A fixed-point iteration strategy. The computer takes a guess vector $v_k$, builds the static matrix $A(v_k)$, extracts its traditional dominant eigenvector to use as the *next* guess $v_{k+1}$, and repeats until the vector stops moving. It is simple but can oscillate wildy if the nonlinearity is too strong.
2. **Newton-Based Methods:** A more aggressive optimization strategy. It treats the problem as a root-finding challenge, looking at the "residual error" gradient to make sharp, mathematically calculated adjustments that force the input and output into rapid alignment.
""")

# ---------------------------------------------------------
# Real-World Applications
# ---------------------------------------------------------
st.markdown("---")
st.markdown("## 🌍 Real-World Applications: Where is this used?")
st.write("Because the matrix transformation updates itself dynamically based on the state vector, the NEPv framework is the underlying math engine for several breakthroughs:")

col_app1, col_app2 = st.columns(2)

with col_app1:
    st.markdown("### 🔬 Quantum Chemistry & Material Science")
    st.markdown(r"""
    When simulating molecules or crystal lattices, the electrostatic forces acting on electrons depend entirely on where the electron cloud density (the state vector $v$) currently resides. 
    
    Solving the **Kohn-Sham equations** in Density Functional Theory (DFT) is fundamentally an NEPv problem. To calculate stable molecular orbits, the matrix and the vector must find perfect harmony.
    """)

with col_app2:
    st.markdown("### 🤖 Machine Learning & Graph Clustering")
    st.markdown(r"""
    In advanced data analysis, traditional linear data cuts often fail to isolate complex groupings. 
    
    By introducing nonlinear constraint matrices that change dynamically based on the partitioning vector, spectral clustering algorithms can isolate intricate, interleaved data communities that traditional standard eigen-solvers pass right through.
    """)

# ---------------------------------------------------------
# Solvers and Pitfalls
# ---------------------------------------------------------
st.markdown("---")
st.markdown(r"""
## 🛠️ How do we solve an NEPv?
Because the matrix changes continuously as $v$ moves, we cannot use standard closed-form algebraic determinants ($\det(A - \lambda I) = 0$). Instead, computers must rely on **iterative numerical methods** to hunt down stable states. 

On this website, you will explore two primary classes of solvers:
1. **Self-Consistent Field (SCF) Iteration:** A fixed-point iteration strategy. The computer takes a guess vector $v_k$, builds the static matrix $A(v_k)$, extracts its traditional dominant eigenvector to use as the *next* guess $v_{k+1}$, and repeats until the vector stops moving.
2. **Newton-Based Methods:** A root-finding challenge. It tracks the "residual error" gradient to make sharp, mathematically calculated vector adjustments to force the input and output into rapid alignment.

### ⚠️ Algorithmic Pitfalls (The Catch)
Numerical optimization isn't always smooth sailing. When you dive into our calculator page, you will observe two classic pitfalls:
""")

col_pit1, col_pit2 = st.columns(2)

with col_pit1:
    st.error("💥 Infinite Oscillations")
    st.markdown("""
    If the nonlinearity weights ($\alpha$ or $\beta$) are scaled up too high, the matrix landscape warps too aggressively. 
    
    Instead of settling down, the **SCF solver** will get caught trapped in an infinite loop, violently bouncing back and forth between two non-solution vectors forever.
    """)

with col_pit2:
    st.error("🕳️ Local Minima & Guess Sensitivity")
    st.markdown("""
    Because nonlinear equations create multi-valley landscapes, changing your starting vector guess ($v_0$) by just a tiny fraction can cause the solver to isolate a completely different equilibrium point—or fail to converge entirely. 
    
    Finding a robust initial guess is often half the battle!
    """)
    
# ---------------------------------------------------------
# Page Navigation Footer
# ---------------------------------------------------------
st.markdown("---")
col_footer1, col_footer2 = st.columns([2, 1])

with col_footer1:
    st.write("Page 1 of 3")

with col_footer2:
    if st.button("➡️ Next: Graphical Visualiser"):
        st.switch_page("pages/2_Graphical_Display.py")
