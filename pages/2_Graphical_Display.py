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
st.markdown("### 🎮 Live Configuration Sandbox")
st.write("Adjust the parameters below to see the 3D space warp in real time.")

# Create a clean side-by-side split: Controls on Left, Graph on Right
col_controls, col_graph = st.columns([1, 2])

with col_controls:
    st.markdown("**Nonlinearity Weights**")
    alpha = st.slider("Weight (α)", 0.0, 4.0, 1.5, 0.1, key="sandbox_alpha")
    beta = st.slider("Weight (β)", 0.0, 4.0, 0.5, 0.1, key="sandbox_beta")
    
    st.markdown("---")
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
    
    # Generate the 3D Plot Object
    fig = plt.figure(figsize=(5, 5))  # Shrunk size to fit neatly inline
    ax = fig.add_subplot(111, projection='3d')
    
    # [Your existing plot background drawing code goes here]
    # e.g., plotting the unit sphere surface mesh, gridlines, etc.
    
    # Plot the active probed vector arrow path
    ax.quiver(0, 0, 0, current_v[0], current_v[1], current_v[2], 
              color="crimson", linewidth=3, label="Probe Vector v")
    
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.legend(loc="upper left")
    
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
# Page Navigation Footer
# ---------------------------------------------------------
st.markdown("---")
col_footer1, col_footer2 = st.columns([2, 1])

with col_footer1:
    st.write("Page 2 of 3")

with col_footer2:
    if st.button("➡️ Next: Examples and Calculator"):
        st.switch_page("pages/3_Examples_and_Solver.py")
