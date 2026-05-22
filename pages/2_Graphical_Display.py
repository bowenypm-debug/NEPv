import streamlit as st
import numpy as np
from scipy.linalg import eig
import matplotlib.pyplot as plt

st.set_page_config(page_title="Graphical Display", layout="wide")

st.title("Graphical Interactive Playground")
st.markdown(r"""
By scaling the problem up to a **$3 \times 3$ system**, our vector $v$ can travel across a **3D Unit Sphere**. 

**Your Objective:** Use the rotation sliders on the left to slide your purple probe vector $v$ smoothly across the 3D space. 
Watch how the 3 distinct system output eigenvectors (red, blue, and green) twist, grow, and shrink in response. 
When your purple vector lines up *perfectly* with any of the dashed output arrows, you have unlocked an equilibrium state of the NEPv!
""")

# ---------------------------------------------------------
# Step 2: Main Workspace - Side-by-Side Sandbox Layout
# ---------------------------------------------------------
st.markdown("Interactive Graphical Playground")
st.write("Adjust the parameters below to see the 3D space warp in real time.")

# Create a clean side-by-side split: Controls on Left, Graph on Right
col_controls, col_graph = st.columns([1, 2])

with col_controls:
    st.markdown("**Nonlinearity Weights**")
    alpha = st.slider("Weight (α)", 0.0, 4.0, 1.5, 0.1, key="sandbox_alpha")
    beta = st.slider("Weight (β)", 0.0, 4.0, 0.5, 0.1, key="sandbox_beta")
    
    st.markdown("**View of Diagram**")
    theta = st.slider("Horizontal Angle", 0.0, 180.0, 45.0, 5.0)
    phi = st.slider("Vertical Angle", 0.0, 360.0, 30.0, 5.0)
    
    # Calculate current state coordinates from angle sliders
    theta_rad = np.radians(theta)
    phi_rad = np.radians(phi)
    current_v = np.array([
        np.sin(theta_rad) * np.cos(phi_rad),
        np.sin(theta_rad) * np.sin(phi_rad),
        np.cos(theta_rad)
    ])

with col_graph:
    # --- Math Calculations Based on Live Sliders ---
    A_curr = np.array([
        [1.0 + alpha * (current_v[0]**2), 0.5, 0.2],
        [0.5, 0.8 + beta * (current_v[1]**2), 0.3],
        [0.2, 0.3, 0.5 + 1.5 * (current_v[2]**2)]
    ])
    
    # Calculate the live eigenvalues/vectors for this configuration state
    vals, vecs = eig(A_curr)
    
    # Generate the 3D Plot Object
    fig = plt.figure(figsize=(5, 5))  # Shrunk size to fit neatly inline
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the 3 live system linear eigenvectors dynamically
    colors = ["#2ECC71", "#3498DB", "#9B59B6"] # Green, Blue, Purple
    for i in range(3):
        ax.quiver(0, 0, 0, vecs[0, i].real, vecs[1, i].real, vecs[2, i].real,
                  color=colors[i], linewidth=2, linestyle="--", 
                  label=f"Eigenvector {i+1} (λ={vals[i].real:.2f})")
    
    # Plot the active probed vector arrow path
    ax.quiver(0, 0, 0, current_v[0], current_v[1], current_v[2], 
              color="crimson", linewidth=4, label="Probe Vector v")
    
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.legend(loc="upper left", bbox_to_anchor=(-0.1, 1.15), fontsize="small")
    
    # Render the smaller figure in the right column
    st.pyplot(fig)

# Display the Matrix Evaluation directly underneath
st.markdown("---")
st.markdown(r"### The 3 $\times$ 3 Matrix Evaluation")
st.write("Your slider positions have constructed the following custom active numerical state matrix:")

st.latex(rf"""
A(v) = \begin{{pmatrix}} 
1.0 + {alpha}({current_v[0]:.2f})^2 & 0.5 & 0.2 \\ 
0.5 & 0.8 + {beta}({current_v[1]:.2f})^2 & 0.3 \\ 
0.2 & 0.3 & 0.5 + 1.5({current_v[2]:.2f})^2
\end{{pmatrix}} = \begin{{pmatrix}} 
{A_curr[0,0]:.2f} & {A_curr[0,1]:.2f} & {A_curr[0,2]:.2f} \\ 
{A_curr[1,0]:.2f} & {A_curr[1,1]:.2f} & {A_curr[1,2]:.2f} \\ 
{A_curr[2,0]:.2f} & {A_curr[2,1]:.2f} & {A_curr[2,2]:.2f} 
\end{{pmatrix}}
""")

st.markdown("##### 💡 Vector Readout Summary:")
st.info(f"Your probe location is currently locked at coordinates:  \n* **X:** `{current_v[0]:.3f}`  \n* **Y:** `{current_v[1]:.3f}`  \n* **Z:** `{current_v[2]:.3f}`")

st.write("Notice how manipulating the rotation parameters bends the output coordinate frames. You can click and drag the canvas background to rotate your perspective view of the entire 3D space field!")

# ---------------------------------------------------------
# NEW INSERTION: Educational Explainer (Leaves all outer code untouched)
# ---------------------------------------------------------
st.markdown("### 🔍 Mathematical Breakdown: What are these arrows?")
st.markdown(f"""
Every time you move the sliders, your vector position inputs are calculated inside the matrix on the left. Because that matrix turns into a temporary set of solid static numbers, it forces open exactly **three specific directional balance axes** based on classic linear algebra:

* <span style="color:#2ECC71">■</span> **Eigenvector 1 (Green dashed arrow):** Target coordinates are `[{vecs[0,0].real:.3f}, {vecs[1,0].real:.3f}, {vecs[2,0].real:.3f}]` with an eigenvalue scale factor of $\lambda = {vals[0].real:.2f}$.
* <span style="color:#3498DB">■</span> **Eigenvector 2 (Blue dashed arrow):** Target coordinates are `[{vecs[0,1].real:.3f}, {vecs[1,1].real:.3f}, {vecs[2,1].real:.3f}]` with an eigenvalue scale factor of $\lambda = {vals[1].real:.2f}$.
* <span style="color:#9B59B6">■</span> **Eigenvector 3 (Purple dashed arrow):** Target coordinates are `[{vecs[0,2].real:.3f}, {vecs[1,2].real:.2f}, {vecs[2,2].real:.3f}]` with an eigenvalue scale factor of $\lambda = {vals[2].real:.2f}$.

Right now, your **Crimson Probe Vector** is resting at coordinates `[{current_v[0]:.3f}, {current_v[1]:.3f}, {current_v[2]:.3f}]`. To solve the **NEPv**, you must nudge the sliders until your crimson vector coordinates perfectly match one of the target sets listed above!
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Page Navigation Footer
# ---------------------------------------------------------
st.markdown("---")
col_footer1, col_footer2 = st.columns([2, 1])

with col_footer1:
    st.write("Page 2 of 3")

with col_footer2:
    if st.button("➡️ Next: Examples and Calculator"):
        st.switch_page("pages/3_Examples_and_Solver.py")
