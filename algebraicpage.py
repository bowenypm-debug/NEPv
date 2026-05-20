import streamlit as st
import numpy as np
from scipy.linalg import eig
import plotly.graph_objects as go

st.set_page_config(page_title="Algebraic Solvers", layout="wide")

st.title("📊 Part 3: Algorithmic Trajectory Tracking")
st.markdown("""
Now that you have discovered solutions *graphically*, let's watch how computers find them *algebraically*. 
Because solutions to an NEPv must satisfy $||v||_2 = 1$, all stable solutions live on the boundary of a **Unit Circle**. 

Pick a starting vector guess below and see how different algorithms navigate the mathematical landscape to hunt for equilibrium.
""")

# ---------------------------------------------------------
# Sidebar System Controls
# ---------------------------------------------------------
st.sidebar.header("🎛️ Global Environment")
alpha = st.sidebar.slider("α (Alpha)", 0.0, 4.0, 1.5, 0.1)
beta = st.sidebar.slider("β (Beta)", 0.0, 4.0, 0.5, 0.1)

# Core Math Functions
def get_A(v, alpha, beta):
    norm = np.linalg.norm(v)
    v_norm = v / norm if norm > 0 else np.array([1.0, 0.0])
    return np.array([
        [1.0 + alpha * (v_norm[0]**2), 1.0],
        [1.0,                         0.5 + beta * (v_norm[1]**2)]
    ])

def run_scf(v_start, alpha, beta, max_iter=15):
    path = [v_start / np.linalg.norm(v_start)]
    v = np.array(path[0])
    
    for _ in range(max_iter):
        A = get_A(v, alpha, beta)
        vals, vecs = eig(A)
        idx = np.argmax(vals.real) # Target the primary dominant mode
        v_next = vecs[:, idx].real
        v_next = v_next / np.linalg.norm(v_next)
        
        # Orient vector to prevent flip-flopping directions on plots
        if np.dot(v, v_next) < 0:
            v_next = -v_next
            
        path.append(v_next)
        if np.allclose(v, v_next, atol=1e-4):
            break
        v = v_next
    return np.array(path)

def run_newton(v_start, alpha, beta, max_iter=15):
    path = [v_start / np.linalg.norm(v_start)]
    v = np.array(path[0])
    
    for _ in range(max_iter):
        A = get_A(v, alpha, beta)
        lam = np.dot(v, A @ v)
        residual = A @ v - lam * v
        
        # Direct local root-correction step
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
# Layout Layout Setup
# ---------------------------------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🎯 Choose Initial Guess ($v_0$)")
    st.write("Where should the algorithms begin their hunt inside the vector space?")
    
    init_x = st.slider("Starting X Coordinate", -1.0, 1.0, 0.8, 0.1)
    init_y = st.slider("Starting Y Coordinate", -1.0, 1.0, -0.6, 0.1)
    
    v_init = np.array([init_x, init_y])
    if np.linalg.norm(v_init) == 0:
        v_init = np.array([1.0, 0.0]) # Handle division by zero protection

    # Run Solvers Natively
    scf_trajectory = run_scf(v_init, alpha, beta)
    newton_trajectory = run_newton(v_init, alpha, beta)
    
    st.markdown("---")
    st.markdown("### 🏎️ Race Results Summary")
    st.write(f"**SCF Iterations taken:** `{len(scf_trajectory) - 1}` steps")
    st.write(f"**Newton Iterations taken:** `{len(newton_trajectory) - 1}` steps")
    
    # Text commentary on pitfalls
    if len(scf_trajectory) > 14:
        st.error("⚠️ **Pitfall Detected (SCF Loop Limit):** The Self-Consistent Field loop failed to settle cleanly and is oscillating endlessly between states because the nonlinearity landscape is warping too fast!")
    else:
        st.success("✅ Both systems converged cleanly to an active solution point.")

with col2:
    st.markdown("### 🗺️ Trajectory Convergence Map")
    st.caption("Track the structural steps taken across the unit sphere coordinate boundary space.")
    
    fig_map = go.Figure()
    
    # 1. Background Unit Circle Ring
    angles = np.linspace(0, 2*np.pi, 100)
    fig_map.add_trace(go.Scatter(
        x=np.cos(angles), y=np.sin(angles),
        mode="lines", line=dict(color="rgba(150,150,150,0.4)", width=1.5, dash="dot"),
        name="Unit Circle Boundary"
    ))
    
    # 2. Add starting marker
    v_norm_start = v_init / np.linalg.norm(v_init)
    fig_map.add_trace(go.Scatter(
        x=[v_norm_start[0]], y=[v_norm_start[1]],
        mode="markers", marker=dict(color="black", size=12, symbol="star"),
        name="Initial Guess (v0)"
    ))
    
    # 3. Add SCF Path
    fig_map.add_trace(go.Scatter(
        x=scf_trajectory[:, 0], y=scf_trajectory[:, 1],
        mode="lines+markers", 
        line=dict(color="#2ECC71", width=3),
        marker=dict(size=8, symbol="circle"),
        name="SCF (Fixed-Point) Path"
    ))
    
    # 4. Add Newton Path
    fig_map.add_trace(go.Scatter(
        x=newton_trajectory[:, 0], y=newton_trajectory[:, 1],
        mode="lines+markers", 
        line=dict(color="#E67E22", width=3),
        marker=dict(size=8, symbol="diamond"),
        name="Newton-Flavor Path"
    ))
    
    fig_map.update_layout(
        xaxis=dict(range=[-1.5, 1.5], zeroline=True, gridcolor="whitesmoke"),
        yaxis=dict(range=[-1.5, 1.5], zeroline=True, gridcolor="whitesmoke"),
        width=550, height=520,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    st.plotly_chart(fig_map, key="solver_trajectory_chart")

# ---------------------------------------------------------
# Educational Breakdown Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("### 📖 Method Deep Dive")

col_info1, col_info2 = st.columns(2)
with col_info1:
    st.info("""
    **Self-Consistent Field (SCF):**
    * **How it works:** It takes the current vector $v_k$, freezing the system matrix state into a normal linear matrix $A(v_k)$. It then computes the regular linear eigenvectors, sets the next state $v_{k+1}$ to the dominant eigenvector output, and repeats.
    * **Pros/Cons:** Incredibly simple to code, but very fragile under strong nonlinearities ($\alpha, \beta > 2.0$), causing it to bounce back and forth indefinitely.
    """)
with col_info2:
    st.warning("""
    **Newton-Based Optimization:**
    * **How it works:** Instead of solving temporary linear problems, it maps out a continuous vector mismatch function, evaluating local geometric gradients to continuously push the vector towards zero system residual error.
    * **Pros/Cons:** Highly robust and mathematically fast near convergence solutions, but requires much higher complex engineering computation formulas per individual step taken.
    """)