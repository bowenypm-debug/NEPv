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
st.markdown("### Interactive Graphical Playground")
st.write("Adjust the coordinates below to aim your probe vector in 3D space.")

# Create a clean side-by-side split: Controls on Left, Graph on Right
col_controls, col_graph = st.columns([1, 2])

with col_controls:
    st.markdown("**Aim Your Probe Vector ($v$)**")
    # Simple, intuitive raw spatial coordinates instead of alpha/beta or angles
    raw_x = st.slider("Position X", -1.0, 1.0, 0.5, 0.1)
    raw_y = st.slider("Position Y", -1.0, 1.0, 0.5, 0.1)
    raw_z = st.slider("Position Z", -1.0, 1.0, 0.7, 0.1)
    
    # Avoid division by zero if all sliders are at 0
    raw_vector = np.array([raw_x, raw_y, raw_z])
    norm = np.linalg.norm(raw_vector)
    if norm == 0:
        current_v = np.array([1.0, 0.0, 0.0])
    else:
        # Normalize so it always lands perfectly on the 3D Unit Sphere
        current_v = raw_vector / norm

    st.markdown("---")
    st.markdown("**View of Diagram**")
    theta = st.slider("Horizontal Camera Angle", 0.0, 180.0, 45.0, 5.0)
    phi = st.slider("Vertical Camera Angle", 0.0, 360.0, 30.0, 5.0)

with col_graph:
    # Hardcoded stable weights for alpha (1.5) and beta (0.5) to keep the NEPv math 
    # perfectly operational underneath without confusing the user with extra sliders.
    alpha_fixed = 1.5
    beta_fixed = 0.5
    
    A_curr = np.array([
        [1.0 + alpha_fixed * (current_v[0]**2), 0.5, 0.2],
        [0.5, 0.8 + beta_fixed * (current_v[1]**2), 0.3],
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
    
    # --- FIXED: Re-apply the camera rotation angles from our sliders ---
    ax.view_init(elev=theta, azim=phi)
    # -------------------------------------------------------------------
    
    ax.legend(loc="upper left", bbox_to_anchor=(-0.1, 1.15), fontsize="small")
    
    # Render the smaller figure in the right column
    st.pyplot(fig)

# Display the Matrix Evaluation directly underneath
st.markdown("---")
st.markdown(r"### The 3 $\times$ 3 Matrix Evaluation")
st.write("Your slider positions have constructed the following custom active numerical state matrix:")

st.latex(rf"""
A(v) = \begin{{pmatrix}} 
1.0 + {alpha_fixed:.1f}({current_v[0]:.2f})^2 & 0.5 & 0.2 \\ 
0.5 & 0.8 + {beta_fixed:.1f}({current_v[1]:.2f})^2 & 0.3 \\ 
0.2 & 0.3 & 0.5 + 1.5({current_v[2]:.2f})^2
\end{{pmatrix}} = \begin{{pmatrix}} 
{A_curr[0,0]:.2f} & {A_curr[0,1]:.2f} & {A_curr[0,2]:.2f} \\ 
{A_curr[1,0]:.2f} & {A_curr[1,1]:.2f} & {A_curr[1,2]:.2f} \\ 
{A_curr[2,0]:.2f} & {A_curr[2,1]:.2f} & {A_curr[2,2]:.2f} 
\end{{pmatrix}}
""")

st.markdown("##### 💡 Vector Readout Summary:")
st.info(f"Your probe location is currently locked at coordinates:  \n* **X:** `{current_v[0]:.3f}`  \n* **Y:** `{current_v[1]:.3f}`  \n* **Z:** `{current_v[2]:.3f}`")

st.write("Notice how manipulating the rotation parameters bends the output coordinate frames. You can use the camera angle sliders to rotate your perspective view of the entire 3D space field!")

st.markdown("### 🔍 The Absolute Basics: What Are These Arrows Telling Us?")

st.markdown("""
If you are completely new to this, the math jargon can look intimidating. Let's break down exactly what is happening in that 3D plot without the technical fluff.

##### 1. What a Matrix Normally Does (The "Blender" vs. The "Stretcher")
Normally, when you multiply a matrix by a vector, it does two things: it **rotates (twists)** the vector in a new direction, and it **scales (stretches or shrinks)** its length. It acts like a space blender.

However, for every matrix, there are a few special, magic directions where **zero twisting happens**. If you point a vector in one of these exact directions:
* The matrix will **only stretch or shrink** the vector.
* The vector stays perfectly on its original line.

* **The Eigenvector** (the dashed arrows) is that magic direction.
* **The Eigenvalue** ($\lambda$) is the scaling factor—how many times longer or shorter the vector gets when pointed there.

##### 2. What Makes a "Nonlinear" Eigenvalue Problem (NEPv) Different?
In standard linear algebra, the landscape is frozen. The magic dashed arrows are glued in place. You just have to find them.

But in this sandbox, we are dealing with a **Nonlinear Eigenvalue Problem (NEPv)**. This means **the landscape changes based on where you look.** 
* The moment you move your **Probe Vector**, the entire matrix morphs (look at the numbers updating in the matrix above!).
* Because the matrix morphs, the magic dashed arrows **move, twist, grow, and shrink in real time.**

##### 3. How to "Win" This Simulation
Right now, your probe vector is pointing in a direction that is being twisted by the matrix. It is *not* in an equilibrium state.

Your goal is to find a sweet spot where **your input causes an output that matches itself**. Look at the live numbers right now:
""")

# Print out clear, intuitive, dynamic comparisons
st.markdown(f"""
* **Your Input Position:** `[{current_v[0]:.2f}, {current_v[1]:.2f}, {current_v[2]:.2f}]`
* <span style="color:#2ECC71">■</span> **Green Target Axis:** If you can guide your probe to `[{vecs[0,0].real:.2f}, {vecs[1,0].real:.2f}, {vecs[2,0].real:.2f}]`, the matrix will only stretch it by a factor of **{vals[0].real:.2f}** without twisting it.
* <span style="color:#3498DB">■</span> **Blue Target Axis:** If you can guide your probe to `[{vecs[0,1].real:.2f}, {vecs[1,1].real:.2f}, {vecs[2,1].real:.2f}]`, the matrix will only stretch it by a factor of **{vals[1].real:.2f}** without twisting it.
* <span style="color:#9B59B6">■</span> **Purple Target Axis:** If you can guide your probe to `[{vecs[0,2].real:.2f}, {vecs[1,2].real:.2f}, {vecs[2,2].real:.2f}]`, the matrix will only stretch it by a factor of **{vals[2].real:.2f}** without twisting it.

**The Ultimate Goal:** Keep adjusting the sliders until your Probe Vector lines up *exactly* on top of one of those dashed lines. When it does, you have solved the NEPv!
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
