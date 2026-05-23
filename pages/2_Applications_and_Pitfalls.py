import streamlit as st

# Real world uses
st.markdown("## Real-World Applications: Where is this used?")
st.write(
    "Because the math formula updates itself as the vector moves, "
    "the NEPv framework is the key to solving some incredible scientific and technological problems:"
)

col_app1, col_app2 = st.columns(2)

with col_app1:
    st.markdown("### 🧪 Quantum Chemistry & Finding Electrons")
    st.markdown(r"""
    When scientists simulate chemical molecules, they need to figure out where electrons are flying. The problem they previously had is that the electrical forces pushing the electrons around depend entirely on where the electron cloud (our vector $v$) currently sits. 
    
    Because the forces shift every time an electron moves, scientists use the NEPv format to find a perfect balance point. Once the formulas and the electron cloud match up exactly the same, it reveals exactly how stable a chemical or material will be in real life.
    """)

with col_app2:
    st.markdown("### 💻 AI & Clustering Data")
    st.markdown(r"""
    In machine learning, computers constantly try to sort complicated data into groups. Traditional math tools can only draw straight lines, which easily fail when data groups are twisted or tangled together. 
    
    By portraying this data as an NEPv framework, the sorting rules automatically warp and bend based on how the data is being grouped which allows the computer to untangle and isolate complex groups of data that standard math methods completely miss.
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
    
    If you pick a starting point that is super far away from a true solution, the algorithms would have to travel a massive distance to get to the true solution. As a result, the calculations can take an excessive number of iterations to find the target.
    """)
    
# Page navigation
st.markdown("---")
col_footer1, col_footer2 = st.columns([3, 1])

with col_footer1:
    st.write("Page 3 of 3")

with col_footer2:
    if st.button("Introduction ↩️", use_container_width=True):
        st.switch_page("Introduction.py")
