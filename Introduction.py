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
    The standard Nonlinear Eigenvalue Problem (NEP) is a problem where the matrix entries depend nonlinearly on the *eigenvalue* parameter itself. This means instead of $\lambda$ having no effect, the entire matrix changes based on a function of $\lambda$, often written as $T(\lambda)$: 
    $$T(\lambda)v = 0$$
    """)

with col3:
    st.markdown("### Level 3: NEPv")
    st.success("**Nonlinear in parameter $\lambda$ and vector $v$**")
    st.markdown(r"""
    In an **NEPv**, the matrix entries depend directly on the *eigenvector* $v$ itself. It uses the form: 
    $$A(v)v = \lambda v$$
    Every time the direction or coordinates of the vector $v$ changes, the values inside the entire matrix $A(v)$ change completely. This is what we want to look at!
    """)

# What is NEPv
st.markdown("---")
st.markdown(r"""
## What does an NEPv actually do?

In a traditional eigenproblem, you are given a specific matrix with set numbers, and your only job is to find the eigenvectors that correspond to it. 

An **NEPv** works completely differently because **the vector you choose actually fills in the numbers of the matrix**. Because the matrix $A(v)$ changes its values depending on the vector $v$ you insert, finding a solution requires achieving a balanced state of **self-consistency**. 

You can think of this process as a continuous loop:
1. You plug in an initial guess vector into the system.
2. The matrix updates its internal numbers based on that vector's coordinates.
3. The matrix then outputs a brand new vector.

If that new output arrow points in the **exact same direction** as the vector you originally put in, the loop balances out, and you have successfully found a solution!
""")

# Page navigation
st.markdown("---")
col_footer1, col_footer2 = st.columns([3, 1])

with col_footer1:
    st.write("Page 1 of 3")

with col_footer2:
    if st.button("Solving Problems ➡️", use_container_width=True):
        st.switch_page("1_Examples_and_Solvers.py")
