import streamlit as st

# Real world uses
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

# Pitfalls
st.markdown("---")
st.markdown(r"""
### Algorithmic Pitfalls (The Catch)
Solving nonlinear math problems isn't always simple and straightforward. When solving an NEPv problem, there are two main pitfalls:
""")

col_pit1, col_pit2 = st.columns(2)

with col_pit1:
    st.error("Infinite Oscillations")
    st.markdown(r"""
    If the numbers in the problem are too large or have a huge difference between them, the possibility of overcorrecting is very high. 
    
    Instead of converging into a single answer, the **SCF loops** can get stuck going back and forth between two different positions forever without ever finding a balance point.
    """)

with col_pit2:
    st.error("Initial Guess Distance")
    st.markdown(r"""
    Because the SCF and Newton based method rely on looping while getting slightly closer on every loop, where you decide to start your initial guess matters a lot. 
    
    If you pick a starting point that is super far away from a true solution, the algorithms would have to travel a massive distance to get to the true solution. As a result, the calculations ca take an excessive number of iterations to find the target.
    """)
    
# Page navigation
st.markdown("---")
col_footer1, col_footer2 = st.columns([3, 1])

with col_footer1:
    st.write("Page 2 of 2")

with col_footer2:
    if st.button("↩️ Introduction", use_container_width=True):
        st.switch_page("Introduction.py")
