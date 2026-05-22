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

# ---------------------------------------------------------
# Step 1: Show an Example Question
# ---------------------------------------------------------
st.subheader("📚 Worked Example Problem")

st.markdown(r"""
To understand how a Nonlinear Eigenvalue Problem works, let's look at a concrete, pure mathematical example.

**The Setup:** Consider a $2 \times 2$ matrix $A(v)$ whose entries directly change depending on the components of the vector $v = \begin{pmatrix} v_1 \\ v_2 \end{pmatrix}$:

$$A(v) = \begin{pmatrix} 1.0 + 1.5|v_1|^2 & 1.0 \\ 1.0 & 0.5 + 0.5|v_2|^2 \end{pmatrix}$$

Our objective is to find a steady-state vector $v$ and a scaling constant $\lambda$ that satisfy the core NEPv equation:
$$A(v)v = \lambda v$$

Let's take an initial guess and see what happens if we guess a simple unit vector $v = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$.

1. **Evaluate the Matrix:** Plugging $v_1 = 1$ and $v_2 = 0$ into our model yields:
   $$A(v) = \begin{pmatrix} 1.0 + 1.5(1)^2 & 1.0 \\ 1.0 & 0.5 + 0.5(0)^2 \end{pmatrix} = \begin{pmatrix} 2.5 & 1.0 \\ 1.0 & 0.5 \end{pmatrix}$$

2. **Compute the Output Product:** Now, we multiply this resulting matrix by our original vector $v$:
   $$A(v)v = \begin{pmatrix} 2.5 & 1.0 \\ 1.0 & 0.5 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 2.5 \\ 1.0 \end{pmatrix}$$

3. **Check for Alignment:** For $v$ to be a solution, the output vector must be a perfect scalar multiple of our input vector. Because $\begin{pmatrix} 2.5 \\ 1.0 \end{pmatrix}$ does not point in the same direction as $\begin{pmatrix} 1 \\ 0 \end{pmatrix}$, **our guess is not a solution.**

**The Goal:** Use the numerical solvers below to find the true coordinate vector where the matrix output aligns perfectly parallel with the input!
""")

# ---------------------------------------------------------
# Step 2: Interactive Custom Matrix Input
# ---------------------------------------------------------
st.markdown("### Design Your Own Matrix Problem")
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

# ---------------------------------------------------------
# Step 3: Trajectory Simulation Display
# ---------------------------------------------------------
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
