import streamlit as st
import numpy as np
from scipy.linalg import eig
import plotly.graph_objects as go

st.set_page_config(page_title="Example and Solvers", layout="wide")

st.title("Part 3: Examples and Calculator")
st.markdown("""
Now that you have discovered solutions *graphically*, let's watch how computers find them *algebraically*. 
Because solutions to an NEPv must satisfy $||v||_2 = 1$, all stable solutions live on the boundary of a **Unit Circle**. 
""")

# ---------------------------------------------------------
# Step 1: Show an Example Question
# ---------------------------------------------------------
st.markdown("### 📝 Worked Example Problem")
with st.expander("🔍 Click to view a typical NEPv Exam/Assignment Question", expanded=True):
    st.markdown("""
    **The Problem:** Consider a system where a particle's energy matrix $A(v)$ changes based on its spatial state vector $v = \begin{pmatrix} v_1 \\ v_2 \end{pmatrix}$. 
    Find the steady-state eigenvector ($A(v)v = \lambda v$) given the nonlinear model:
    
    $$A(v) = \begin{pmatrix} 1.0 + 1.5|v_1|^2 & 1.0 \\ 1.0 & 0.5 + 0.5|v_2|^2 \end{pmatrix}$$
    
    *   **Analytical Insight:** If $v = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$, then $A(v) = \begin{pmatrix} 2.5 & 1.0 \\ 1.0 & 0.5 \end{pmatrix}$. Notice that $A(v)v = \begin{pmatrix} 2.5 \\ 1.0 \end{pmatrix}$, which is **not** parallel to $v$. Thus, $\begin{pmatrix} 1 \\ 0 \end{pmatrix}$ is *not* a solution.
    *   **The Goal:** Use the solvers below to find the true vector where the output aligns perfectly with the input.
    """)

# ---------------------------------------------------------
# Step 2: Interactive Custom Matrix Input
# ---------------------------------------------------------
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
with col_mat_in4:
    st.markdown("**Your Active Equation Setup:**")
    st.latex(rf"""
    A(v) = \begin{pmatrix} 
    {base_a11} + \alpha|v_1|^2 & {off_diag} \\ 
    {off_diag} & {base_a22} + \beta|v_2|^2 
    \end{pmatrix}
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
    st.write(f"**Newton-Flavor Iterations:** `{len(newton_trajectory) - 1}` steps")
    
    if len(scf_trajectory) > 14:
        st.error("⚠️ **Solver Pitfall:** SCF is stuck oscillating endlessly! The landscape is warping too aggressively for it to balance.")
    else:
        st.success("✅ Solvers successfully isolated a steady-state solution.")
        st.write(f"**Final Calculated Vector:** `[{scf_trajectory[-1][0]:.3f}, {scf_trajectory[-1][1]:.3f}]`")

with col2:
    fig_map = go.Figure()
    
    # Background Unit Circle
    angles = np.linspace(0, 2*np.pi, 100)
    fig_map.add_trace(go.Scatter(
        x=np.cos(angles), y=np.sin(angles),
        mode="lines", line=dict(color="rgba(150,150,150,0.4)", width=1.5, dash="dot"),
        name="Unit Circle Boundary"
    ))
    
    # Start Point
    v_norm_start = v_init / np.linalg.norm(v_init)
    fig_map.add_trace(go.Scatter(
        x=[v_norm_start[0]], y=[v_norm_start[1]],
        mode="markers", marker=dict(color="black", size=12, symbol="star"),
        name="Initial Guess (v0)"
    ))
    
    # Paths
    fig_map.add_trace(go.Scatter(
        x=scf_trajectory[:, 0], y=scf_trajectory[:, 1],
        mode="lines+markers", line=dict(color="#2ECC71", width=3),
        marker=dict(size=8), name="SCF Path"
    ))
    fig_map.add_trace(go.Scatter(
        x=newton_trajectory[:, 0], y=newton_trajectory[:, 1],
        mode="lines+markers", line=dict(color="#E67E22", width=3),
        marker=dict(size=8, symbol="diamond"), name="Newton-Flavor Path"
    ))
    
    fig_map.update_layout(
        xaxis=dict(range=[-1.5, 1.5], zeroline=True, gridcolor="whitesmoke"),
        yaxis=dict(range=[-1.5, 1.5], zeroline=True, gridcolor="whitesmoke"),
        width=550, height=450,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_map, key="solver_trajectory_chart")
# ---------------------------------------------------------
# Page Navigation Footer
# ---------------------------------------------------------
st.markdown("---")
col_footer1, col_footer2 = st.columns([2, 1])

with col_footer1:
    st.write("Page 3 of 3")

with col_footer2:
    if st.button("↩️ Introduction", use_container_width=True):
        st.switch_page("Home.py")
