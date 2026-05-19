import streamlit as st
import numpy as np
from scipy.linalg import eig
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configurations & Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="NEPv Interactive Visualizer",
    page_icon="📐",
    layout="wide"
)

st.title("🧩 Exploring Nonlinear Eigenvalue Problems (NEPv)")
st.markdown("""
In a standard eigenvalue problem, the matrix $A$ is fixed. In an **NEPv**, the matrix *depends on its own eigenvector*: $A(v)v = \lambda v$.
Use this application to explore this phenomenon both **graphically** (by moving an input vector) and **algebraically** (by tracing numerical solvers).
""")

# Sidebar Controls for Nonlinearity
st.sidebar.header("🎛️ System Parameters")
alpha = st.sidebar.slider("Nonlinearity Weight (α - Alpha)", 0.0, 4.0, 1.5, 0.1)
beta = st.sidebar.slider("Nonlinearity Weight (β - Beta)", 0.0, 4.0, 0.5, 0.1)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 How to use the Graphical Mode:")
st.sidebar.write("1. Click anywhere on the left **Input Vector** grid.")
st.sidebar.write("2. The right plot will update with the frozen eigenvalues/vectors of $A(v)$.")
st.sidebar.write("3. **Challenge:** Try to align the purple input vector $v$ with either the red or blue output eigenvectors!")

# ---------------------------------------------------------
# Core Mathematical Engine
# ---------------------------------------------------------
def get_A(v, alpha, beta):
    """Computes the state of matrix A given vector v."""
    norm = np.linalg.norm(v)
    v_norm = v / norm if norm > 0 else np.array([1.0, 0.0])
    
    # Simple NEPv system: diagonal elements scale with the square of v components
    A = np.array([
        [1.0 + alpha * (v_norm[0]**2), 1.0],
        [1.0,                         0.5 + beta * (v_norm[1]**2)]
    ])
    return A

def run_scf(v_start, alpha, beta, max_iter=15):
    """Runs Self-Consistent Field (SCF) iterations."""
    path = [v_start / np.linalg.norm(v_start)]
    v = np.array(path[0])
    
    for _ in range(max_iter):
        A = get_A(v, alpha, beta)
        vals, vecs = eig(A)
        # Track the dominant eigenvector trajectory
        idx = np.argmax(vals.real)
        v_next = vecs[:, idx].real
        v_next = v_next / np.linalg.norm(v_next)
        
        # Enforce consistency in sign/direction for a clean plot
        if np.dot(v, v_next) < 0:
            v_next = -v_next
            
        path.append(v_next)
        if np.allclose(v, v_next, atol=1e-4):
            break
        v = v_next
    return np.array(path)

def run_newton(v_start, alpha, beta, max_iter=15):
    """
    Simplified Newton-step approach minimizing the residual 
    R(v) = A(v)v - (v^T A(v) v)v.
    """
    path = [v_start / np.linalg.norm(v_start)]
    v = np.array(path[0])
    
    for _ in range(max_iter):
        A = get_A(v, alpha, beta)
        lam = np.dot(v, A @ v)
        residual = A @ v - lam * v
        
        # Take a gradient-descent flavored correction step as a Newton analog
        v_next = v - 0.3 * residual 
        v_next = v_next / np.linalg.norm(v_next)
        
        if np.dot(v, v_next) < 0:
            v_next = -v_next
            
        path.append(v_next)
        if np.linalg.norm(residual) < 1e-4:
            break
        v = v_next
    return np.array(path)

# ---------------------------------------------------------
# Tabs for Modes
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["🔮 Graphical Mode (Live Drag/Click)", "📊 Algebraic Mode (Solvers)"])

with tab1:
    st.subheader("Interactive Vector Sandbox")
    
    # Coordinate State Keeping for interactive clicking
    if "click_coord" not in st.session_state:
        st.session_state.click_coord = {"x": 1.0, "y": 0.5}

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Click inside the plot to change the vector $v$:**")
        
        # Base Plotly Input Graph
        fig_in = go.Figure()
        fig_in.add_trace(go.Scatter(
            x=[0, st.session_state.click_coord["x"]],
            y=[0, st.session_state.click_coord["y"]],
            mode="lines+markers+text",
            text=["", "  v (Input)"],
            textposition="top right",
            line=dict(color="purple", width=4),
            marker=dict(size=10, color="purple"),
            name="Your Vector v"
        ))
        
        fig_in.update_layout(
            xaxis=dict(range=[-2, 2], zeroline=True, gridcolor="lightgray"),
            yaxis=dict(range=[-2, 2], zeroline=True, gridcolor="lightgray"),
            width=450, height=450,
            clickmode="event+select",
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        # Capture the click coordinates natively from Streamlit
        ed = st.plotly_chart(fig_in, key="input_chart", on_select="rerun")
        
        if ed and ed.get("selection") and ed["selection"]["points"]:
            # Capture where user clicked on the graph grid
            pt = ed["selection"]["points"][0]
            st.session_state.click_coord["x"] = pt["x"]
            st.session_state.click_coord["y"] = pt["y"]

    with col2:
        st.markdown("**Resulting Eigenvectors of the frozen matrix $A(v)$:**")
        
        current_v = np.array([st.session_state.click_coord["x"], st.session_state.click_coord["y"]])
        A_curr = get_A(current_v, alpha, beta)
        vals, vecs = eig(A_curr)
        
        # Plotting Output Eigenvectors
        fig_out = go.Figure()
        colors = ["red", "blue"]
        
        for idx in range(2):
            v_eigen = vecs[:, idx].real * vals[idx].real
            fig_out.add_trace(go.Scatter(
                x=[0, v_eigen[0]], y=[0, v_eigen[1]],
                mode="lines+markers+text",
                text=["", f" λ{idx+1}={vals[idx].real:.2f}"],
                textposition="top center",
                line=dict(color=colors[idx], width=3, dash="dash"),
                name=f"Eigenvector {idx+1}"
            ))
            
        fig_out.update_layout(
            xaxis=dict(range=[-4, 4], zeroline=True, gridcolor="lightgray"),
            yaxis=dict(range=[-4, 4], zeroline=True, gridcolor="lightgray"),
            width=450, height=450,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_out, key="output_chart")

with tab2:
    st.subheader("Algorithm Trajectory Tracking")
    st.write("See how mathematical solvers step through the space to target a true system solution state from a starting point.")
    
    col_al_1, col_al_2 = st.columns([1, 2])
    
    with col_al_1:
        st.markdown("### Algorithmic Parameters")
        start_x = st.slider("Initial Target X Component", -1.0, 1.0, 0.8, 0.1)
        start_y = st.slider("Initial Target Y Component", -1.0, 1.0, -0.6, 0.1)
        v_start = np.array([start_x, start_y])
        
        if np.linalg.norm(v_start) == 0:
            v_start = np.array([1.0, 0.0])
            
        scf_path = run_scf(v_start, alpha, beta)
        newton_path = run_newton(v_start, alpha, beta)
        
    with col_al_2:
        # Plotting the mathematical pathing
        fig_path = go.Figure()
        
        # Unit circle reference
        theta = np.linspace(0, 2*np.pi, 100)
        fig_path.add_trace(go.Scatter(
            x=np.cos(theta), y=np.sin(theta),
            mode="lines", line=dict(color="gray", width=1, dash="dot"),
            name="Unit Vector Sphere Boundary"
        ))
        
        # Plot SCF Steps
        fig_path.add_trace(go.Scatter(
            x=scf_path[:, 0], y=scf_path[:, 1],
            mode="lines+markers", line=dict(color="green", width=2),
            marker=dict(symbol="circle", size=8),
            name="SCF Convergence Path"
        ))
        
        # Plot Newton Steps
        fig_path.add_trace(go.Scatter(
            x=newton_path[:, 0], y=newton_path[:, 1],
            mode="lines+markers", line=dict(color="orange", width=2),
            marker=dict(symbol="diamond", size=8),
            name="Newton-Flavor Path"
        ))
        
        fig_path.update_layout(
            xaxis=dict(range=[-1.5, 1.5], zeroline=True),
            yaxis=dict(range=[-1.5, 1.5], zeroline=True),
            width=600, height=500,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        st.plotly_chart(fig_path, key="trajectory_chart")