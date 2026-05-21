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
    st.markdown("### Level 2: Standard NEP")
    st.warning("**Nonlinear in Parameter $\lambda$**")
    st.markdown(r"""
    In a standard Nonlinear Eigenvalue Problem (NEP), the matrix entries depend nonlinearly on the *eigenvalue* parameter itself, often written as $T(\lambda)$. 
    $$T(\lambda)v = 0$$
    This is frequently used in mechanical vibrations and structural engineering.
    """)

with col3:
    st.markdown("### Level 3: The NEPv")
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
# Page Navigation Footer
# ---------------------------------------------------------
st.markdown("---")
col_footer1, col_footer2 = st.columns([2, 1])

with col_footer1:
    st.write("Page 1 of 3")

with col_footer2:
    if st.button("➡️ Next: Graphical Visualiser"):
        st.switch_page("pages/2_Graphical_Display.py")
