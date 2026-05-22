import streamlit as st
import numpy as np
from scipy.linalg import eig
import matplotlib.pyplot as plt

st.set_page_config(page_title="Example and Calculator", layout="wide")

st.title("Part 3: Examples and Calculator")
st.markdown("""
Now that you have discovered solutions *graphically*, let's watch how computers find them *algebraically*. 
Because solutions to an NEPv must satisfy $||v||_2 = 1$, all stable solutions live on the boundary of a **Unit Circle**. 
""")

# =========================================================================
# 1. SCF Deep Dive & Collapsible Worked Example
# =========================================================================
st.subheader("1. Strategy A: The Self-Consistent Field (SCF) Loop")
st.markdown(r"""
Imagine you are standing in front of a magical, warped mirror. When you move, the mirror itself bends and changes shape. Your goal is to find a spot where your reflection points in the **exact same direction** you are standing.

The **Self-Consistent Field (SCF)** strategy handles this changing mirror with a simple "freeze-and-step" game:
1. **Stand on a spot** ($v_0$) and look at the mirror.
2. **Freeze time.** Calculate exactly how the mirror looks based *only* on where you are currently standing.
3. **Look at the reflection** that the frozen mirror throws out.
4. **Step to that new reflection spot** ($v_1$). 
5. **Unfreeze time, and repeat.**

If you keep stepping to where the mirror tells you to go, you hope the mirror stops warping and you both settle down into a perfect balance. This state of balance is what mathematicians call **self-consistency**.
""")

with st.expander("📊 View This Step By Step Worked Example Question Using SCF (2 by 2)"):
    st.markdown(r"""
    Let's watch how this algorithm plays the game using our baseline problem:
    $$A(v) = \begin{pmatrix} 1.0 + 1.5|v_1|^2 & 1.0 \\ 1.0 & 0.5 + 0.5|v_2|^2 \end{pmatrix}$$
    
    **Step 0: Our First Guess**  
    Let's point our vector straight along the X-axis: 
    $$v_0 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$$
    
    **Iteration 1: Freezing the Mirror**  
    We plug our coordinates ($v_1 = 1, v_2 = 0$) into the formula. This temporarily locks the mirror into a regular, static grid:
    $$A(v_0) = \begin{pmatrix} 1.0 + 1.5(1)^2 & 1.0 \\ 1.0 & 0.5 + 0.5(0)^2 \end{pmatrix} = \begin{pmatrix} 2.5 & 1.0 \\ 1.0 & 0.5 \end{pmatrix}$$
    
    We ask this frozen grid: *"Where do you want to point things?"* The strongest direction this specific grid naturally pushes vectors toward is:
    $$\text{Reflection} \approx \begin{pmatrix} 0.943 \\ 0.332 \end{pmatrix}$$
    
    So, our algorithm takes a step and updates our position to that exact spot:
    $$v_1 = \begin{pmatrix} 0.943 \\ 0.332 \end{pmatrix}$$
    
    **Iteration 2: The Next Loop**  
    Now we are standing at a new spot ($v_1 = 0.943, v_2 = 0.332$). Because we moved, the mirror warps again! We calculate its new frozen shape:
    $$A(v_1) \approx \begin{pmatrix} 2.334 & 1.0 \\ 1.0 & 0.555 \end{pmatrix}$$
    
    This new shape throws out a slightly different reflection:
    $$v_2 \approx \begin{pmatrix} 0.912 \\ 0.410 \end{pmatrix}$$
    
    With every loop, the amount the mirror changes gets smaller and smaller, until our input position and the mirror's output direction line up perfectly!
    """)

st.markdown("---")

# =========================================================================
# 2. Newton Method Deep Dive & Collapsible Worked Example
# =========================================================================
st.subheader("2. Strategy B: The Newton-Based Error Fixer")
st.markdown(r"""
SCF is simple, but it has a weakness: if the mirror warps too violently when you move, you might end up wildly bouncing back and forth forever without ever settling down.

**Newton-based methods** use a smarter, more active steering strategy. Instead of just blindly stepping wherever the reflection points, it measures your **miss distance** (the error):
$$\text{Error} = \text{Where the mirror points your reflection} - \text{Where you are standing} = \vec{0}$$

Think of it like driving a car:
* Instead of waiting to see where the wind blows you, you actively look at how far you are drifting off the center line.
* If you look down and see you are drifting too far to the right, you intentionally steer to the left to cancel out the error.

Because it actively calculates how to fix its own mistakes using the local "slope" of the landscape, Newton's method can sprint to a solution much faster than SCF. However, because it relies on local steering cues, if you start with a terrible initial guess, it might panic, steer off the road, and get completely lost!
""")

with st.expander("📊 View This Step By Step Worked Example Question Using Newton Based Methods (2 by 2)"):
    st.markdown(r"""
    Using the same setup as in the SCF example, we can try solving it with Newton Based Method \\
    $$A(v) = \begin{pmatrix} 1.0 + 1.5|v_1|^2 & 1.0 \\ 1.0 & 0.5 + 0.5|v_2|^2 \end{pmatrix}$$
    
    **Step 0: Checking the Mismatch**  
    We start at our same guess: pointing straight along the X-axis: $v_0 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$. 
    
    When we push this vector through the matrix, it outputs a reflection pointing at $\begin{pmatrix} 2.5 \\ 1.0 \end{pmatrix}$. 
    
    **Step 1: Measuring the Error**  
    We compare where the reflection pointed against where we aimed. After scaling things to keep the lengths fair, we find our structural mismatch:
    $$\text{Error Vector} = \begin{pmatrix} 0 \\ 1.0 \end{pmatrix}$$
    
    This tells the solver: *"Your X-coordinate is fine, but your reflection is spilling over too much on the Y-axis by a value of $+1.0$."*
    
    **Step 2: Actively Correcting the Course**  
    To cancel that error out, the Newton solver takes our original position and subtracts a fraction of that error (nudging it in the opposite direction):
    $$v_{\text{corrected}} = \begin{pmatrix} 1 \\ 0 \end{pmatrix} - 0.4 \cdot \begin{pmatrix} 0 \\ 1.0 \end{pmatrix} = \begin{pmatrix} 1 \\ -0.4 \end{pmatrix}$$
    
    We pull this new position back onto our unit circle boundary so it stays a proper unit pointer:
    $$v_1 \approx \begin{pmatrix} 0.928 \\ -0.371 \end{pmatrix}$$
    
    Notice how this single, clever calculation immediately yanks the vector into the correct quadrant to find the balancing point!
    """)

# =========================================================================
# 3. Interactive Custom Matrix Input (Kept Exactly Same)
# =========================================================================
st.markdown("---")
st.markdown("### 🛠️ Design Your Own Matrix Problem")
st.write("Modify the base parameters below to see how your own custom NEPv configuration behaves.")

col_mat_in1, col_mat_in2, col_mat_in3, col_mat_in4 = st.columns(4)
with col_mat_in1:
    base_a11 = st.number_input("Base A11", value=1.0, step=0.1)
    alpha = st.slider("Nonlinearity Weight (α)", 0.0, 4.0, 1.5, 0.1)
with col_mat_in2:
    off_diag = st.number_input("Off-Diagonal (A12 & A21)", value=1.0, step=0.1)
with col_mat_in3:
    base_a22 = st.number_input("Base A22", value=0.5, step=0.1)
    beta = st.slider("Nonlinearity Weight (β)", 0.0, 4.0, 0.5, 0.1)

st.markdown("Your Active Equation Setup:")
st.latex(rf"""
A(v) = \begin{{pmatrix}} 
{base_a11} + {alpha}|v_1|^2 & {off_diag} \\ 
{off_diag} & {base_a22} + {beta}|v_2|^2 
\end{{pmatrix}}
""")

# Core Math Functions using Custom User Variables
def get_custom_A(v):
    norm = np.linalg.norm(v)
    v_norm = v / norm if norm > 0 else np.array([1.0, 0.0])
    return np.array([
        [base_a11 + alpha * (v_norm[0]**2), off_diag],
        [off_diag,                         base_a22 + beta * (v_norm[1]**2)]
    ])

def run_scf(v_start, max_iter=15):
    path = [v_start / np.linalg.norm(v_start)]
    v = np.array(path[0])
    for _ in range(max_iter):
        A = get_custom_A(v)
        vals, vecs = eig(A)
        idx = np.argmax(vals.real) 
        v_next = vecs[:, idx].real
        v_next = v_next / np.linalg.norm(v_next)
        if np.dot(v, v_next) < 0:
            v_next = -v_next
        path.append(v_next)
        if np.allclose(v, v_next, atol=1e-4):
            break
        v = v_next
    return np.array(path)

def run_newton(v_start, max_iter=15):
    path = [v_start / np.linalg.norm(v_start)]
    v = np.array(path[0])
    for _ in range(max_iter):
        A = get_custom_A(v)
        lam = np.dot(v, A @ v)
        residual = A @ v - lam * v
        v_next = v - 0.4 * residual 
        v_next = v_next / np.linalg.norm(v_next)
        if np.dot(v, v_next) < 0:
            v_next = -v_next
        path.append(v_next)
        if np.linalg.norm(residual) < 1e-4:
            break
        v = v_next
    return np.array(path)

# =========================================================================
# 4. Trajectory Simulation Display (Kept Exactly Same)
# =========================================================================
st.markdown("---")
st.markdown("### 🏃‍♂️ Run the Solvers")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("##### Choose Initial Guess ($v_0$)")
    init_x = st.slider("Starting X Coordinate", -1.0, 1.0, 0.8, 0.1)
    init_y = st.slider("Starting Y Coordinate", -1.0, 1.0, -0.6, 0.1)
    
    v_init = np.array([init_x, init_y])
    if np.linalg.norm(v_init) == 0:
        v_init = np.array([1.0, 0.0])

    scf_trajectory = run_scf(v_init)
    newton_trajectory = run_newton(v_init)
    
    st.markdown("##### 🏁 Race Results")
    st.write(f"**SCF Iterations:** `{len(scf_trajectory) - 1}` steps")
    st.write(f"**Newton Iterations:** `{len(newton_trajectory) - 1}` steps")
    
    if len(scf_trajectory) > 14:
        st.error("⚠️ **Solver Pitfall:** SCF is stuck oscillating endlessly! The landscape is warping too aggressively for it to balance.")
    else:
        st.success("✅ Solvers successfully isolated a steady-state solution.")
        st.write(f"**Final Calculated Vector:** `[{scf_trajectory[-1][0]:.3f}, {scf_trajectory[-1][1]:.3f}]`")

with col2:
    # Build Matplotlib figure object
    fig_map, ax = plt.subplots(figsize=(6, 6))
    
    # 1. Plot a perfect reference Unit Circle Boundary
    angles = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(angles), np.sin(angles), color="darkgray", linestyle="--", linewidth=1.5, label="Unit Circle Boundary")
    
    # 2. Plot the initial starting guess vector position marked with a distinct star symbol
    v_norm_start = v_init / np.linalg.norm(v_init)
    ax.plot(v_norm_start[0], v_norm_start[1], marker="*", color="black", markersize=14, linestyle="None", zorder=5, label="Initial Guess ($v_0$)")
    
    # 3. Plot the step-by-step Self-Consistent Field (SCF) mathematical iteration trajectory
    ax.plot(scf_trajectory[:, 0], scf_trajectory[:, 1], marker="o", color="#2ECC71", linewidth=2.5, markersize=6, label="SCF Path")
    
    # 4. Plot the step-by-step Newton optimization trajectory
    ax.plot(newton_trajectory[:, 0], newton_trajectory[:, 1], marker="d", color="#E67E22", linewidth=2.5, markersize=6, label="Newton Path")
    
    # Grid system formatting updates
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.axhline(0, color='silver', linewidth=1)
    ax.axvline(0, color='silver', linewidth=1)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left", framealpha=0.9)
    
    # Render figure directly onto your webpage layout canvas
    st.pyplot(fig_map)

# ---------------------------------------------------------
# Page Navigation Footer
# ---------------------------------------------------------
st.markdown("---")
col_footer1, col_footer2 = st.columns([3, 1])

with col_footer1:
    st.write("Page 3 of 3")

with col_footer2:
    if st.button("↩️ Introduction", use_container_width=True):
        st.switch_page("Introduction.py")
