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
st.subheader("1. The Self-Consistent Field (SCF) Iteration")
st.markdown(r"""
The **Self-Consistent Field (SCF)** approach (often called linear freezing) breaks down a nonlinear problem into a repeating loop of standard linear algebra questions. 

Instead of trying to handle the shifting landscape all at once, SCF simplifies the process:
1. Start with an initial guess vector $v_0$.
2. Plug that vector into your equations to **freeze** the nonlinear terms, creating a temporary, standard linear matrix: $A_{\text{temp}} = A(v_0)$.
3. Solve for the traditional linear eigenvalues and eigenvectors of $A_{\text{temp}}$.
4. Select the output eigenvector that points closest to your original guess, normalize it, and make it your updated guess $v_1$.
5. Repeat this cycle until the vector stops changing ($v_k \approx v_{k+1}$). When the input vector matches the output eigenvector, you have achieved *self-consistency*.
""")

with st.expander("📊 View Step-by-Step Worked Example Question Using SCF (2 by 2)"):
    st.markdown(r"""
    Let's look at how the SCF algorithm handles our baseline matrix problem:
    
    $$A(v) = \begin{pmatrix} 1.0 + 1.5|v_1|^2 & 1.0 \\ 1.0 & 0.5 + 0.5|v_2|^2 \end{pmatrix}$$
    
    **Step 0: Initial Guess**  
    Let's guess a simple starting unit vector lying fully on the X-axis: 
    $$v_0 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$$
    
    **Iteration 1: Freezing the Matrix**  
    We plug $v_1 = 1$ and $v_2 = 0$ into the nonlinear formulas to lock in a static linear matrix:
    $$A(v_0) = \begin{pmatrix} 1.0 + 1.5(1)^2 & 1.0 \\ 1.0 & 0.5 + 0.5(0)^2 \end{pmatrix} = \begin{pmatrix} 2.5 & 1.0 \\ 1.0 & 0.5 \end{pmatrix}$$
    
    Next, we find the linear eigenvectors of this frozen matrix. The dominant eigenvector (the one with the largest eigenvalue, $\lambda \approx 2.85$) is:
    $$e_{\text{max}} \approx \begin{pmatrix} 0.943 \\ 0.332 \end{pmatrix}$$
    
    Since this is the closest available linear eigenvector to our original guess, we select and normalize it to establish our next update:
    $$v_1 = \begin{pmatrix} 0.943 \\ 0.332 \end{pmatrix}$$
    
    **Iteration 2: The Next Loop**  
    Now, we repeat the freezing process using our updated coordinates ($v_1 = 0.943, v_2 = 0.332$):
    $$A(v_1) = \begin{pmatrix} 1.0 + 1.5(0.943)^2 & 1.0 \\ 1.0 & 0.5 + 0.5(0.332)^2 \end{pmatrix} \approx \begin{pmatrix} 2.334 & 1.0 \\ 1.0 & 0.555 \end{pmatrix}$$
    
    Computing the dominant linear eigenvector for this newly warped matrix yields:
    $$v_2 \approx \begin{pmatrix} 0.912 \\ 0.410 \end{pmatrix}$$
    
    With every loop, the difference between the input vector and the resulting output vector shrinks. Within a few more steps, the updates will lock onto a static coordinate where the input and output match perfectly!
    """)

st.markdown("---")

# =========================================================================
# 2. Newton Method Deep Dive & Collapsible Worked Example
# =========================================================================
st.subheader("2. Newton-Based Optimization Methods")
st.markdown(r"""
While SCF is highly intuitive, it can struggle or oscillate endlessly if the nonlinear warping is too aggressive. **Newton-based methods** take a completely different geometric strategy by converting the problem into a root-finding challenge.

We construct a residual function $F(v)$ that tracks our total balance error. For an exact solution, the matrix product minus the scaled vector must equal zero:
$$F(v) = A(v)v - \lambda v = \vec{0}$$

Instead of passively waiting for an eigenvector loop to settle, a Newton solver evaluates the local slope of this error landscape (using derivatives or step-by-step differences). With each step, it senses the steepness under its feet and takes a deliberate jump directly down the path toward zero:
$$v_{k+1} = v_k - \Delta v$$

* **The Advantage:** When your guess gets reasonably close to a solution, Newton-based optimization exhibits incredibly fast convergence, narrowing in on the target coordinates in very few steps.
* **The Disadvantage:** Because it relies heavily on local slopes, a poor initial guess can occasionally cause the algorithm to lose its footing and jump entirely in the wrong direction.
""")

with st.expander("📊 View Step-by-Step Worked Example Question Using Newton Based Methods (2 by 2)"):
    st.markdown(r"""
    Using the same question setup as the SCF method of:
    $$A(v) = \begin{pmatrix} 1.0 + 1.5|v_1|^2 & 1.0 \\ 1.0 & 0.5 + 0.5|v_2|^2 \end{pmatrix}$$
    
    **Step 0: The Current State**  
    Imagine we are sitting at our initial guess vector $v_0 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$. As we calculated earlier, the matrix output at this point is:
    $$A(v_0)v_0 = \begin{pmatrix} 2.5 \\ 1.0 \end{pmatrix}$$
    
    The Rayleigh quotient gives us our current estimated scaling factor ($\lambda = v^T A v = 2.5$).
    
    **Step 1: Measuring the Residual (Error)**  
    We calculate our directional error vector $F(v_0)$ by checking how far our output misses a perfect scalar match:
    $$F(v_0) = A(v_0)v_0 - \lambda v_0 = \begin{pmatrix} 2.5 \\ 1.0 \end{pmatrix} - 2.5 \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 0 \\ 1.0 \end{pmatrix}$$
    
    This tells the solver that the vector has zero error along the X-axis, but a significant structural mismatch of $+1.0$ pointing along the Y-axis.
    
    **Step 2: The Newton Correction Jump**  
    Using a step-scaling factor (like the $0.4$ multiplier used in our playground engine below), the algorithm alters the vector coordinates in the opposite direction of the error to push it downhill toward zero:
    $$v_{\text{raw}} = v_0 - 0.4 \cdot F(v_0) = \begin{pmatrix} 1 \\ 0 \end{pmatrix} - \begin{pmatrix} 0 \\ 0.4 \end{pmatrix} = \begin{pmatrix} 1 \\ -0.4 \end{pmatrix}$$
    
    Finally, we project this raw jump back onto our unit boundary circle to preserve our required scaling length ($||v||_2 = 1$):
    $$v_1 = \frac{v_{\text{raw}}}{||v_{\text{raw}}||} \approx \begin{pmatrix} 0.928 \\ -0.371 \end{pmatrix}$$
    
    Notice how this single, calculated step immediately shifts the vector into the correct quadrant to find the balancing point!
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
