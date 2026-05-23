# Real world uses
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
    If the numbers in the problem are too large or have a huge different between them, the possibility of overcorrecting is very high. 
    
    Instead of settling down to a single answer, the **SCF solver** gets stuck on a mathematical seesaw—violently slamming back and forth between two different positions forever without ever finding a balance point.
    """)

with col_pit2:
    st.error("Guess Sensitivity")
    st.markdown("""
    Because nonlinear problems create complex landscapes with many different valleys, your starting point matters immensely. 
    
    Changing your initial vector guess ($v_0$) by just a tiny hair can cause the computer to slide into a completely different balance point—or miss all of them entirely. Finding a good starting guess is often half the battle!
    """)
    
# Page navigation
st.markdown("---")
col_footer1, col_footer2 = st.columns([3, 1])

with col_footer1:
    st.write("Page 2 of 2")

with col_footer2:
    if st.button("↩️ Introduction", use_container_width=True):
        st.switch_page("Introduction.py")
