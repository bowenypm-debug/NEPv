import streamlit as st

st.set_page_config(page_title="NEPv Introduction", layout="wide")

st.title("An Introduction to Nonlinear Eigenvalue Problems (NEPv)")
st.markdown("---")

st.markdown(r"""
Welcome! This interactive website is designed to guide you through the theory, geometry, and computation a fascinating yet highly advanced linear algebra topic: **Nonlinear Eigenvalue Problem with Eigenvector Depedency (NEPv)**.

To understand what an NEPv is and why it is unique, lets first look at the topic in three distinct levels of difficulty.
""")

# 3 eigenvalue/eigenvector problem levels
st.markdown("## 🪜 The Three Levels of Eigenvalue/Eigenvector Problems")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Level 1: Traditional")
    st.info("**Linear Eigenproblem**")
    st.markdown(r"""
    In a traditional eigenproblem, we look at a specific, fixed matrix $A$. You look for a scalar $\lambda$ known as the eigenvalue and a non zero vector $v$ corresponding to the scalar $\lambda$ known as the eigenvector such that:
    $$Av = \lambda v$$.
    The matrix $A$ will never change in this case. It acts as a fixed linear transformation on the vector space.
    """)

with col2:
    st.markdown("### Level 2: NEP")
    st.warning("**Nonlinear in parameter $\lambda$**")
    st.markdown(r"""
    The standard Nonlinear Eigenvalue Problem (NEP) is a problem where the matrix entries depend nonlinearly on the *eigenvalue* parameter itself meaning that matrix entries don't depend on being a scalar $\lambda$ with a power of one but depend based on a function, often written as $T(\lambda)$. 
    $$T(\lambda)v = 0$$
    """)

with col3:
    st.markdown("### Level 3: NEPv")
    st.success("**Nonlinear in parameter $\lambda$ and vector $v$**")
    st.markdown(r"""
    In an **NEPv**, the matrix entries depend directly on the state or coordinates of the *eigenvector* itself. 
    $$A(v)v = \lambda v$$
    As the vector $v$ changes position, the entire matrix landscape warps and mutates. This is what we want to look at!
    """)

# ---------------------------------------------------------
# What is an NEPv & How do we solve it?
# ---------------------------------------------------------
st.markdown("---")
st.markdown(r"""
## What does an NEPv actually do?

In a traditional math problem, finding an eigenvector is like following a fixed trail on a map—the trail stays exactly where it is while you walk on it. 

In an **NEPv**, it is like trying to find a path through deep sand or snow where **your footsteps actively alter the ground beneath you**. Because the matrix $A(v)$ alters its values depending on the vector $v$ you insert, computing a final answer requires finding a balanced state of **self-consistency**. 

Think of it as a perfect feedback loop: you feed a vector into the matrix formula, the matrix updates its numbers based on that vector, and then outputs a directional arrow that points in that exact same direction. 

This framework is highly critical in advanced computational sciences, such as tracking electron clouds in quantum chemistry or isolating interconnected data groups in machine learning.

---

## How do we solve an NEPv?

Because the matrix grid continuously changes shape as the vector moves, we cannot use standard algebraic shortcuts from regular class (like calculating determinants by hand). Instead, computers have to use **running guessing loops** to hunt down stable balance points. 

On this website, you will explore two primary ways computers do this:

1. **Self-Consistent Field (SCF) Iteration (The Simple Loop):** The computer takes a starting guess vector, plugs it into the matrix formula to freeze it into a standard matrix, calculates the traditional eigenvector for that matrix, and sets that result as the *new* guess. It repeats this cycle over and over until the input and output match. It is easy to build, but it can panic and bounce back and forth if the rules change too violently.
2. **Newton-Based Methods (The Smart Correction):** Instead of just blindly calculating a new arrow at every step, this method measures the exact **error** between your current guess and a true solution. It then makes smart, calculated adjustments to subtract that error away, steering the vector directly toward a balanced target.
""")

# ---------------------------------------------------------
# Real-World Applications
# ---------------------------------------------------------
st.markdown("---")
st.markdown("## Real-World Applications: Where is this used?")
st.write("Because the matrix transformation updates itself dynamically based on the state vector, the NEPv framework is the underlying math engine for several breakthroughs:")

col_app1, col_app2 = st.columns(2)

with col_app1:
    st.markdown("### Quantum Chemistry & Material Science")
    st.markdown(r"""
    When simulating molecules or crystal lattices, the electrostatic forces acting on electrons depend entirely on where the electron cloud density (the state vector $v$) currently resides. 
    
    Solving the **Kohn-Sham equations** in Density Functional Theory (DFT) is fundamentally an NEPv problem. To calculate stable molecular orbits, the matrix and the vector must find perfect harmony.
    """)

with col_app2:
    st.markdown("### Machine Learning & Graph Clustering")
    st.markdown(r"""
    In advanced data analysis, traditional linear data cuts often fail to isolate complex groupings. 
    
    By introducing nonlinear constraint matrices that change dynamically based on the partitioning vector, spectral clustering algorithms can isolate intricate, interleaved data communities that traditional standard eigen-solvers pass right through.
    """)

# ---------------------------------------------------------
# Solvers and Pitfalls
# ---------------------------------------------------------
st.markdown("---")
st.markdown(r"""
### Algorithmic Pitfalls (The Catch)
Solving nonlinear math problems isn't always smooth sailing. When you dive into our calculator page, you will get to see two classic pitfalls firsthand:
""")

col_pit1, col_pit2 = st.columns(2)

with col_pit1:
    st.error("Infinite Oscillations")
    st.markdown(r"""
    If you turn the nonlinearity settings up too high, the matrix landscape reacts too drastically to changes. 
    
    Instead of settling down to a single answer, the **SCF solver** gets stuck on a mathematical seesaw—violently slamming back and forth between two different positions forever without ever finding a balance point.
    """)

with col_pit2:
    st.error("Guess Sensitivity")
    st.markdown("""
    Because nonlinear problems create complex landscapes with many different valleys, your starting point matters immensely. 
    
    Changing your initial vector guess ($v_0$) by just a tiny hair can cause the computer to slide into a completely different balance point—or miss all of them entirely. Finding a good starting guess is often half the battle!
    """)
    
# ---------------------------------------------------------
# Page Navigation Footer
# ---------------------------------------------------------
st.markdown("---")
col_footer1, col_footer2 = st.columns([2, 1])

with col_footer1:
    st.write("Page 1 of 2")

with col_footer2:
    if st.button("➡️ Next: Solving Problems"):
        st.switch_page("pages/2_Examples_and_Solvers.py")
