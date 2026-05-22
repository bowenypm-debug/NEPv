import streamlit as st
import numpy as np
from scipy.linalg import eig
import matplotlib.pyplot as plt

st.set_page_config(page_title="Graphical Display", layout="wide")

st.title("Graphical Interactive Playground")

# ---------------------------------------------------------
# Step 1: The Explainer - Concept Primer at the Top
# ---------------------------------------------------------
st.markdown("### 🔍 The Absolute Basics: What Are We Looking At?")
st.markdown("""
Before diving into the interactive simulator below, let's establish a quick mental model of how matrices twist and stretch space without getting bogged down in dense mathematics.

##### 1. The Matrix as a "Space Blender"
Normally, when you multiply a matrix by a vector, it forces that vector to change in two ways: it **rotates (twists)** the vector into a new direction, and it **scales (stretches or shrinks)** its overall length. 

However, every matrix has a few special, unique directions where **zero twisting happens**. If you align a vector precisely along one of these magic paths:
* The matrix will **only stretch or shrink** the vector.
* The vector stays locked perfectly on its original structural line.

In linear algebra, this un-twisted direction is called an **Eigenvector** (represented by the dashed lines below), and its scaling multiplier is called an **Eigenvalue** ($\lambda$).

##### 2. What Makes a "Nonlinear" Problem Different?
In standard textbook linear algebra, the landscape is completely frozen. The magic dashed target lines are glued permanently in place, and your only job is to calculate where they sit.

But in this sandbox, we are exploring a **Nonlinear Eigenvalue Problem (NEPv)**. Here, **the landscape morphs based on where you look.** 
* The moment you alter your **Probe Vector** coordinates, the numbers inside the transformation matrix recalculate in real time.
* Because the underlying matrix itself is constantly shifting, the target dashed lines will **bend, twist, grow, and shrink dynamically as you move.**
""")

st.markdown("---")

# ---------------------------------------------------------
# Step 2: Main Workspace - Side-by-Side Sandbox Layout
# ---------------------------------------------------------
st.markdown("### Interactive Graphical Playground")
st.markdown(r"""
**Your Objective:** Adjust the position sliders on the left to slide your Crimson Probe Vector $v$ smoothly through 3D space. 
Watch how the green, blue, and purple target lines twist away from you. Keep tweaking your direction until your solid Crimson Vector **lines up perfectly** on top of any of the dashed output arrows. 
When they snap into alignment, you have discovered an equilibrium state—a true solution to the Nonlinear Eigenvalue Problem!
""")

# Create a clean side-by-side split: Controls on Left, Graph on Right
col_controls, col_graph = st.columns([1, 2])

with col_controls:
    st.markdown("**Aim Your Probe Vector ($v$)**")
    # Simple, intuitive raw spatial coordinates instead of alpha/beta or angles
    raw_x = st.slider("Position X", -1.0, 1.0, 0.5, 0.1)
    raw_y = st.slider("Position Y", -1.0, 1.0, 0.5, 0.1)
    raw_z = st.slider("Position Z", -1.0, 1.0, 0.7, 0.1)
    
    raw_vector = np.array([raw_x, raw_y, raw_z])
    current_norm = np.linalg.norm(raw_vector)
    
    # Enforce a maximum magnitude of 1.0 instead of scaling everything to 1.0
    if current_norm > 1.0:
        current_v = raw_vector / current_norm
        norm_v = 1.0
    else:
        current_v = raw_vector
        norm_v = current_norm

    st.markdown("---")
    st.markdown("**View of Diagram**")
    theta = st.slider("Horizontal Camera Angle", 0.0, 360.0, 45.0, 5.0)
    phi = st.slider("Vertical Camera Angle", 0.0, 180.0, 30.0, 5.0)

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
              color="crimson", linewidth=4, label="Probe Vector v", arrow_length_ratio=0.1 if norm_v > 0 else 0)
    
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    
    # Correctly mapping camera perspective controls
    ax.view_init(elev=phi, azim=theta)
    
    ax.legend(loc="upper left", bbox_to_anchor=(-0.1, 1.15), fontsize="small")
    
    # Render the smaller figure in the right column
    st.pyplot(fig)

# ---------------------------------------------------------
# Step 3: Mathematical Matrix Evaluation Readout
# ---------------------------------------------------------
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

# Dynamic live target values context block
st.markdown(f"""
##### Live Target Comparison:
* **Your Input Position:** `[{current_v[0]:.2f}, {current_v[1]:.2f}, {current_v[2]:.2f}]`
* <span style="color:#2ECC71">■</span> **Green Target Axis:** If you can guide your probe to `[{vecs[0,0].real:.2f}, {vecs[1,0].real:.2f}, {vecs[2,0].real:.2f}]`, the matrix will only stretch it by a factor of **{vals[0].real:.2f}**.
* <span style="color:#3498DB">■</span> **Blue Target Axis:** If you can guide your probe to `[{vecs[0,1].real:.2f}, {vecs[1,1].real:.2f}, {vecs[2,1].real:.2f}]`, the matrix will only stretch it by a factor of **{vals[1].real:.2f}**.
* <span style="color:#9B59B6">■</span> **Purple Target Axis:** If you can guide your probe to `[{vecs[0,2].real:.2f}, {vecs[1,2].real:.2f}, {vecs[2,2].real:.2f}]`, the matrix will only stretch it by a factor of **{vals[2].real:.2f}**.
""", unsafe_allow_html=True)

st.write("Notice how manipulating the rotation parameters bends the output coordinate frames. You can use the camera sliders to rotate your perspective view of the entire 3D space field!")

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
