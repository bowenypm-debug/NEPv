import streamlit as st
import numpy as np
from scipy.linalg import eig
import plotly.graph_objects as go

st.set_page_config(page_title="Graphical Sandbox", layout="wide")

st.title("🔮 Part 2: Graphical Intuition Sandbox")
st.markdown("""
In this sandbox, you can see how changing the input vector $v$ shifts the underlying matrix operator. 

**Your Objective:** Try to click around the graph on the left to move the purple vector $v$. Watch how the red and blue output eigenvectors stretch and rotate in response. 
If you can make the purple vector point **exactly in the same direction** as either the red or blue dashed vectors, you have manually discovered a solution to the NEPv!
""")

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.header("🎛️ Nonlinearity Weights")
alpha = st.sidebar.slider("α (Alpha - affects horizontal stretching)", 0.0, 4.0, 1.5, 0.1)
beta = st.sidebar.slider("β (Beta - affects vertical stretching)", 0.0, 4.0, 0.5, 0.1)

# Helper function to compute the dynamic matrix
def get_A(v, alpha, beta):
    norm = np.linalg.norm(v)
    v_norm = v / norm if norm > 0 else np.array([1.0, 0.0])
    
    # Dynamic matrix system where components warp the diagonal field
    A = np.array([
        [1.0 + alpha * (v_norm[0]**2), 1.0],
        [1.0,                         0.5 + beta * (v_norm[1]**2)]
    ])
    return A

# ---------------------------------------------------------
# State Keeping & Layout
# ---------------------------------------------------------
if "click_coord" not in st.session_state:
    st.session_state.click_coord = {"x": 1.0, "y": 0.5}

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🗺️ 1. Choose Input Vector $v$")
    st.caption("Click anywhere inside this grid to reposition the probe vector.")
    
    # Draw the interactive input vector plot
    fig_in = go.Figure()
    
    # Add a subtle background reference unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    fig_in.add_trace(go.Scatter(
        x=np.cos(theta), y=np.sin(theta),
        mode="lines", line=dict(color="rgba(200,200,200,0.5)", width=1, dash="dot"),
        showlegend=False
    ))
    
    # Draw the actual input vector
    fig_in.add_trace(go.Scatter(
        x=[0, st.session_state.click_coord["x"]],
        y=[0, st.session_state.click_coord["y"]],
        mode="lines+markers+text",
        text=["", "  v (Input)"],
        textposition="top right",
        line=dict(color="#884EA2", width=4),
        marker=dict(size=10, color="#884EA2"),
        showlegend=False
    ))
    
    fig_in.update_layout(
        xaxis=dict(range=[-2, 2], zeroline=True, zerolinecolor="black", gridcolor="lightgray"),
        yaxis=dict(range=[-2, 2], zeroline=True, zerolinecolor="black", gridcolor="lightgray"),
        width=450, height=450,
        clickmode="event+select",
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Listen to selection changes from the Streamlit canvas interaction
    event_data = st.plotly_chart(fig_in, key="sandbox_input_chart", on_select="rerun")
    
    if event_data and event_data.get("selection") and event_data["selection"]["points"]:
        pt = event_data["selection"]["points"][0]
        st.session_state.click_coord["x"] = pt["x"]
        st.session_state.click_coord["y"] = pt["y"]

with col2:
    st.markdown("### ⚡ 2. Resulting System Spectrum")
    st.caption("These are the calculated linear eigenvectors/values for your frozen state matrix.")
    
    current_v = np.array([st.session_state.click_coord["x"], st.session_state.click_coord["y"]])
    A_curr = get_A(current_v, alpha, beta)
    vals, vecs = eig(A_curr)
    
    # Draw the dynamic resulting output system vectors
    fig_out = go.Figure()
    colors = ["#E74C3C", "#3498DB"] # Red and Blue
    
    for idx in range(2):
        # Scale the unit eigenvector by its calculated value magnitude for visual display
        v_eigen = vecs[:, idx].real * vals[idx].real
        fig_out.add_trace(go.Scatter(
            x=[0, v_eigen[0]], y=[0, v_eigen[1]],
            mode="lines+markers+text",
            text=["", f" λ{idx+1} = {vals[idx].real:.2f}"],
            textposition="top center",
            line=dict(color=colors[idx], width=3, dash="dash"),
            name=f"Eigenvector {idx+1}"
        ))
        
    fig_out.update_layout(
        xaxis=dict(range=[-4, 4], zeroline=True, zerolinecolor="black", gridcolor="lightgray"),
        yaxis=dict(range=[-4, 4], zeroline=True, zerolinecolor="black", gridcolor="lightgray"),
        width=450, height=450,
        legend=dict(yanchor="bottom", y=0.01, xanchor="left", x=0.01),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_out, key="sandbox_output_chart")

# ---------------------------------------------------------
# Dynamic Explanation Content Block
# ---------------------------------------------------------
st.markdown("---")
st.markdown("### 🔍 Live Matrix Inspection")

col_mat1, col_mat2 = st.columns([1, 2])

with col_mat1:
    st.write("Your choices have built this temporary matrix operator state:")
    st.latex(rf"""
    A(v) = \begin{pmatrix} 
    1.0 + {alpha}({current_v[0]:.2f})^2 & 1.0 \\ 
    1.0 & 0.5 + {beta}({current_v[1]:.2f})^2 
    \end{pmatrix} = \begin{pmatrix} 
    {A_curr[0,0]:.2f} & {A_curr[0,1]:.2f} \\ 
    {A_curr[1,0]:.2f} & {A_curr[1,1]:.2f} 
    \end{pmatrix}
    """)

with col_mat2:
    st.markdown("##### 🧪 Observation Insight:")
    if alpha == 0 and beta == 0:
        st.success("Lineär Mode: Notice how dragging the purple vector changes nothing on the right graph! Because α and β are zero, the matrix values are entirely frozen.")
    elif alpha > 2.5 or beta > 2.5:
        st.warning("High Nonlinearity: Because your scaling factors are large, notice how moving the purple vector just a fraction of an inch wildly swings the direction of the target dashed output states. This extreme warping is exactly what makes finding mathematical convergence so difficult.")
    else:
        st.info("Standard Nonlinearity Mode: Moving your input vector dynamically shifts the weights along the diagonal matrix positions, dragging the system's principal modes along with it.")