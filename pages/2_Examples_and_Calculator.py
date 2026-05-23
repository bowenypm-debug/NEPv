import streamlit as st
import numpy as np
from scipy.linalg import eig
import matplotlib.pyplot as plt

st.set_page_config(page_title="Examples and Solvers", layout="wide")

st.title("Part 2: Algebraic Solvers & Examples")
st.markdown("""
Before we map out these problems visually, let's explore how we actually solve Nonlinear Eigenvalue Problem (NEPv) algebraically. 
Because any valid solution vector must satisfy the normalization constraint $||v||_2 = 1$, all steady-state solutions live precisely on the boundary of a unit circle.
""")

# =========================================================================
# 1. SCF Section
# =========================================================================
st.subheader("Method 1: Self-Consistent Field (SCF)")
st.markdown(r"""
In a standard linear eigenvalue problem, you solve $Av = \lambda v$ where the matrix $A$ is a static constant. In a Nonlinear Eigenvalue Problem (NEPv), the matrix entries change depending on the vector $v$ you plug into it. This is commonly written in the mathematical form:

$$H(v)v = \lambda v$$

The **Self-Consistent Field (SCF)** method solves this by turning the nonlinear equation into a loop of traditional linear problems:

1. **Choose an initial guess** vector ($v_0$).
2. **Plug your guess into the formula** to calculate a fixed, standard matrix: $H(v_0)$.
3. **Compute the traditional eigenvectors** of this fixed matrix.
4. **Update your next guess** ($v_1$) to be the resulting eigenvector.
5. **Repeat the loop** until the vector that we plug into the matrix formula and the resulting eigenvector is exactly the same meaning $v_k \approx v_{k+1}$.

When the input vector and the output eigenvector perfectly match, the system has achieved *self-consistency*, meaning you have successfully isolated a true solution to the nonlinear equation.
""")

with st.expander("📊 View this step by step worked example question using SCF (2 by 2)"):
    st.markdown(r"""
    Let's calculate the first few steps using our baseline problem matrix:
    $$H(v) = \begin{pmatrix} 1.0 + 1.5|v_1|^2 & 1.0 \\ 1.0 & 0.5 + 0.5|v_2|^2 \end{pmatrix}$$
    
    **Step 0: Choose an Initial Guess**  
    We select a simple starting unit vector pointing along the X-axis: 
    $$v_0 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$$
    
    **Iteration 1: Plugging the Guess in**  
    We plug our coordinates ($v_1 = 1, v_2 = 0$) into the matrix formula. This yields a standard, static linear matrix:
    $$H(v_0) = \begin{pmatrix} 1.0 + 1.5(1)^2 & 1.0 \\ 1.0 & 0.5 + 0.5(0)^2 \end{pmatrix} = \begin{pmatrix} 2.5 & 1.0 \\ 1.0 & 0.5 \end{pmatrix}$$
    
    Next, we calculate the standard linear eigenvectors for this fixed matrix $H(v_0)$. The dominant eigenvector (the one corresponding to the largest eigenvalue) is:
    $$\text{Resulting Eigenvector} \approx \begin{pmatrix} 0.943 \\ 0.332 \end{pmatrix}$$
    
    We update our next guess to this result:
    $$v_1 = \begin{pmatrix} 0.943 \\ 0.332 \end{pmatrix}$$
    
    **Iteration 2: Repeating the Process**  
    Now we take our new updated vector ($v_1 = 0.943, v_2 = 0.332$) and plug it back into the original matrix formula to get our next linear matrix $H(v_1)$:
    $$H(v_1) \approx \begin{pmatrix} 2.334 & 1.0 \\ 1.0 & 0.555 \end{pmatrix}$$
    
    Computing the dominant standard eigenvector for this updated matrix gives us our next step:
    $$v_2 \approx \begin{pmatrix} 0.912 \\ 0.410 \end{pmatrix}$$
    
    With each iteration, the difference between the vector we plug into $H(v)$ and the eigenvector we get out shrinks, tracking a direct path toward a stable equilibrium.
    """)

st.markdown("---")

# =========================================================================
# 2. Newton Section
# =========================================================================
st.subheader("Method 2: Newton-Based Methods")
st.markdown(r"""
While SCF simply updates the vector step-by-step using the latest eigenvector, it can struggle or oscillate endlessly if the matrix entries in $H(v)$ change too rapidly. **Newton-based methods** take a more mathematical approach by explicitly measuring our balance error.

Using our common form $H(v)v = \lambda v$, if we group everything on one side, we can define a **residual vector (the error)** that tracks how far away our current guess is from a true solution:
$$\text{Residual} = H(v)v - \lambda v$$

If our vector is a perfect solution, the residual vector will equal exactly $\vec{0}$. 

Instead of resetting our guess completely to the new eigenvector like SCF does, Newton's method calculates the algebraic "slope" of this residual error. It calculates exactly how changing our coordinates will minimize the error, and then takes a calculated step to subtract that error from our position:
$$v_{k+1} = v_k - \Delta v$$

* **The Advantage:** Once your guess is reasonably close to a solution, Newton's method converges rapidly because it is mathematically calculating the shortest path to bring the residual error to zero.
* **The Disadvantage:** It requires a decent initial guess. Because it relies heavily on local slopes, a bad starting guess can cause the calculation to overshoot and fail to converge.
""")

with st.expander("📊 View this step by step worked example question using Newton based method (2 by 2)"):
    st.markdown(r"""
    Let's look at how Newton's method calculates its algebraic adjustments using our initial position.
    
    **Step 0: Evaluate the Current Residual**  
    We start at our initial guess: $v_0 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$. 
    
    Multiplying this vector by our evaluated matrix yields the product vector $H(v_0)v_0 = \begin{pmatrix} 2.5 \\ 1.0 \end{pmatrix}$. Using the standard Rayleigh quotient ($v^T H(v) v$), our current eigenvalue estimate is $\lambda = 2.5$.
    
    **Step 1: Calculate the Error Vector**  
    We check how far off our matrix product is from a perfect scalar multiple:
    $$\text{Residual Vector} = H(v_0)v_0 - \lambda v_0 = \begin{pmatrix} 2.5 \\ 1.0 \end{pmatrix} - 2.5 \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 0 \\ 1.0 \end{pmatrix}$$
    
    This shows the solver that the current guess has zero balancing error along the X-axis, but a structural mismatch of $+1.0$ pointing along the Y-axis.
    
    **Step 2: Apply the Mathematical Correction**  
    The Newton solver modifies our vector by subtracting a fraction of this residual vector to damp out the error (the playground engine below uses a step multiplier of $0.4$):
    $$v_{\text{raw}} = v_0 - 0.4 \cdot \text{Residual} = \begin{pmatrix} 1 \\ 0 \end{pmatrix} - \begin{pmatrix} 0 \\ 0.4 \end{pmatrix} = \begin{pmatrix} 1 \\ -0.4 \end{pmatrix}$$
    
    Finally, because a valid eigenvector must be a normalized unit vector, we project it back onto our boundary circle:
    $$v_1 = \frac{v_{\text{raw}}}{||v_{\text{raw}}||} \approx \begin{pmatrix} 0.928 \\ -0.371 \end{pmatrix}$$
    
    Notice how this structured algebraic step immediately shifts the vector coordinates toward the correct quadrant to resolve the mismatch!
    """)

# =========================================================================
# 3. Interactive Custom Matrix Input
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
# 4. Trajectory Simulation Display
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
    st.write("Page 2 of 3")

with col_footer2:
    if st.button("➡️ Graphical Visualizer", use_container_width=True):
        st.switch_page("3_Graphical_Sandbox.py")
