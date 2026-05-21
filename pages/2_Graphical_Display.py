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
# Sidebar Controls (Angles & Nonlinearity)
# ---------------------------------------------------------
st.sidebar.header("🕹️ Vector Orientation Controls")
theta = st.sidebar.slider("Horizontal Rotation (θ - Theta)", 0.0, 360.0, 45.0, 5.0)
phi = st.sidebar.slider("Vertical Tilt Angle (ϕ - Phi)", 0.0, 180.0, 60.0, 5.0)

st.sidebar.header("🎛️ Nonlinearity Weights")
alpha = st.sidebar.slider("α (Alpha)", 0.0, 4.0, 2.0, 0.1)
beta = st.sidebar.slider("β (Beta)", 0.0, 4.0, 1.0, 0.1)

# Convert Angles to a 3D Unit Vector
theta_rad = np.radians(theta)
phi_rad = np.radians(phi)
x = np.sin(phi_rad) * np.cos(theta_rad)
y = np.sin(phi_rad) * np.sin(theta_rad)
z = np.cos(phi_rad)
current_v = np.array([x, y, z])

# Define the dynamic 3x3 NEPv System Matrix
def get_A_3d(v, alpha, beta):
    # A symmetric 3x3 matrix where diagonals depend heavily on the vector's position
    A = np.array([
        [1.0 + alpha * (v[0]**2), 0.5,                     0.2],
        [0.5,                     0.8 + beta * (v[1]**2),  0.3],
        [0.2,                     0.3,                     0.5 + 1.5 * (v[2]**2)]
    ])
    return A

# Compute current matrix state spectrum
A_curr = get_A_3d(current_v, alpha, beta)
vals, vecs = eig(A_curr)

# ---------------------------------------------------------
# Matplotlib 3D Engine Setup
# ---------------------------------------------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Draw a faint 3D reference wireframe unit sphere
u = np.linspace(0, 2 * np.pi, 30)
w = np.linspace(0, np.pi, 30)
sphere_x = np.outer(np.cos(u), np.sin(w))
sphere_y = np.outer(np.sin(u), np.sin(w))
sphere_z = np.outer(np.ones(np.size(u)), np.cos(w))
ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color="gray", alpha=0.15, linewidth=0.5)

# Plot 1: Draw the User's Purple Input Probe Vector (v)
ax.quiver(0, 0, 0, current_v[0], current_v[1], current_v[2], 
          color="purple", linewidth=4, arrow_length_ratio=0.15, label="Input Vector (v)")

# Plot 2: Draw the 3 output eigenvectors scaling them by their real eigenvalues
colors = ["#E74C3C", "#3498DB", "#2ECC71"] # Red, Blue, Green
for idx in range(3):
    v_eigen = vecs[:, idx].real
    eigenval = vals[idx].real
    # Draw arrow scaling outward from the origin
    ax.quiver(0, 0, 0, v_eigen[0] * eigenval, v_eigen[1] * eigenval, v_eigen[2] * eigenval,
              color=colors[idx], linewidth=2.5, linestyle="--", arrow_length_ratio=0.1,
              label=f"Eigenvector {idx+1} (λ={eigenval:.2f})")

# Graphic Formatting
ax.set_xlim([-2.5, 2.5])
ax.set_ylim([-2.5, 2.5])
ax.set_zlim([-2.5, 2.5])
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.legend(loc="upper left")
ax.grid(True, linestyle=":", alpha=0.5)

# Render columns layout in Streamlit
col_viz, col_mat = st.columns([3, 2])

with col_viz:
    st.pyplot(fig)

with col_mat:
    st.markdown(r"### Live 3 $\times$ 3 Matrix Evaluation")
    st.write("Your slider positions have constructed the following custom active numerical state:")
    
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
    st.info(f"Your probe location is currently locked at coordinates:\n* **X:** `{current_v[0]:.3f}`\n* **Y:** `{current_v[1]:.3f}`\n* **Z:** `{current_v[2]:.3f}`")
    
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
