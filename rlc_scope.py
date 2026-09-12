import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal

# 1. Page Configuration
st.set_page_config(
    page_title="RLC-Scope Pro | Mathematical & Physics Solvation Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS UI Styling (Dark Glassmorphism Theme)
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        font-family: 'Inter', sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        margin-bottom: 24px;
    }
    .main-title {
        color: #f8fafc;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.0rem;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .math-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .card-label {
        color: #38bdf8;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Application Header
st.markdown("""
<div class="main-header">
    <div class="main-title">⚡ RLC-Scope Pro</div>
    <div class="sub-title">Complex Mathematical Solvation Engine, Complex Impedance & Phasor Vector Analysis</div>
</div>
""", unsafe_allow_html=True)

# 4. Sidebar Input Controls
st.sidebar.markdown("### 🔌 Source Inputs")
V_in = st.sidebar.slider("Source Voltage (V_in) [V_rms]", 1.0, 100.0, 12.0, step=0.5)
f_ac = st.sidebar.slider("Operating Frequency (f) [Hz]", 10.0, 10000.0, 1000.0, step=10.0)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Circuit Components")
R = st.sidebar.slider("Resistance (R) [Ω]", 0.1, 500.0, 25.0, step=0.5)
L_mH = st.sidebar.slider("Inductance (L) [mH]", 0.1, 100.0, 10.0, step=0.1)
C_uF = st.sidebar.slider("Capacitance (C) [µF]", 0.1, 100.0, 5.0, step=0.5)

st.sidebar.markdown("---")
colorscale_choice = st.sidebar.selectbox("3D Surface Map Theme", ["Viridis", "Plasma", "Turbo", "Electric", "Cividis"])

# Unit Conversions
L = L_mH / 1000.0       # Henries
C = C_uF / 1000000.0    # Farads
omega_ac = 2 * np.pi * f_ac

# 5. Advanced Mathematical & Complex AC Solvation Engine
XL = omega_ac * L
XC = 1 / (omega_ac * C) if omega_ac > 0 else 0
X_net = XL - XC
Z_complex = complex(R, X_net)
Z_mag = np.abs(Z_complex)
phase_rad = np.angle(Z_complex)
phase_deg = np.degrees(phase_rad)

# RMS Currents & Phasor Voltages
I_complex = V_in / Z_complex if Z_mag > 0 else 0
I_rms = np.abs(I_complex)

V_R_complex = I_complex * R
V_L_complex = I_complex * complex(0, XL)
V_C_complex = I_complex * complex(0, -XC)

# Resonance, Bandwidth & Q-Factor
omega_0 = 1 / np.sqrt(L * C)
f_0 = omega_0 / (2 * np.pi)
Q_factor = (1 / R) * np.sqrt(L / C) if R > 0 else 0
BW_hz = f_0 / Q_factor if Q_factor > 0 else 0
f_lower = f_0 - (BW_hz / 2)
f_upper = f_0 + (BW_hz / 2)

# Power Calculations (Complex Triangle)
S_complex = V_in * np.conj(I_complex)
P_real = S_complex.real                         # Active Power (Watts)
Q_reactive = S_complex.imag                     # Reactive Power (VAR)
S_apparent = np.abs(S_complex)                  # Apparent Power (VA)
PF = np.cos(phase_rad)                          # Power Factor

# Natural Transient Differential Solvation
alpha = R / (2 * L)
zeta = alpha / omega_0
discriminant = alpha**2 - omega_0**2

if zeta < 1.0:
    state_label = "Underdamped"
    omega_d = np.sqrt(omega_0**2 - alpha**2)
    s1 = complex(-alpha, omega_d)
    s2 = complex(-alpha, -omega_d)
    eq_form = r"v(t) = B e^{-\alpha t} \sin(\omega_d t + \phi)"
elif zeta == 1.0:
    state_label = "Critically Damped"
    omega_d = 0.0
    s1 = complex(-alpha, 0)
    s2 = complex(-alpha, 0)
    eq_form = r"v(t) = (B_1 + B_2 t) e^{-\alpha t}"
else:
    state_label = "Overdamped"
    omega_d = 0.0
    s1 = complex(-alpha + np.sqrt(discriminant), 0)
    s2 = complex(-alpha - np.sqrt(discriminant), 0)
    eq_form = r"v(t) = B_1 e^{s_1 t} + B_2 e^{s_2 t}"

# LTI Transfer Function Solvation
num = [1]
den = [L * C, R * C, 1]
sys = signal.TransferFunction(num, den)
t, v_out = signal.impulse(sys)
v_out = v_out * V_in

# 6. Top Metrics Bar
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Complex Impedance (|Z|)", f"{Z_mag:.2f} Ω")
m2.metric("RMS Current (I_rms)", f"{I_rms*1000:.1f} mA")
m3.metric("Quality Factor (Q)", f"{Q_factor:.2f}")
m4.metric("Bandwidth (Δf)", f"{BW_hz:.1f} Hz")
m5.metric("Damping Ratio (ζ)", f"{zeta:.3f}")

st.markdown("<br>", unsafe_allow_html=True)

# 7. Tabbed Interface Setup
tab1, tab2, tab3 = st.tabs(["🧮 Explicit Mathematical Solvation", "📈 Visualizations & Phasor Vectors", "⚡ Power & Resonance Physics"])

with tab1:
    st.markdown("### 🧮 Step-by-Step Analytical Solvation Engine")
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        st.markdown("""
        <div class="math-card">
            <div class="card-label">1. Complex Impedance & Reactance Formulation</div>
        """, unsafe_allow_html=True)
        st.latex(rf"X_L = 2\pi f L = 2\pi({f_ac})({L_mH}\times 10^{{-3}}) = {XL:.2f}\,\Omega")
        st.latex(rf"X_C = \frac{{1}}{{2\pi f C}} = \frac{{1}}{{2\pi({f_ac})({C_uF}\times 10^{{-6}})}} = {XC:.2f}\,\Omega")
        st.latex(rf"\mathbf{{Z}} = R + j(X_L - X_C) = {R:.1f} + j({X_net:.2f})\,\Omega")
        st.latex(rf"|\mathbf{{Z}}| = \sqrt{{{R:.1f}^2 + ({X_net:.2f})^2}} = {Z_mag:.2f}\,\Omega, \quad \phi = {phase_deg:.2f}^\circ")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="math-card">
            <div class="card-label">2. Transfer Function H(s) & Characteristic Roots</div>
        """, unsafe_allow_html=True)
        st.latex(r"H(s) = \frac{1}{LC s^2 + RC s + 1} = \frac{\omega_0^2}{s^2 + 2\alpha s + \omega_0^2}")
        st.latex(rf"\alpha = \frac{{R}}{{2L}} = {alpha:.2f}\,\text{{rad/s}}, \quad \omega_0 = \frac{{1}}{{\sqrt{{LC}}}} = {omega_0:.2f}\,\text{{rad/s}}")
        if zeta < 1.0:
            st.latex(rf"s_{{1,2}} = -\alpha \pm j\omega_d = {-alpha:.2f} \pm j{omega_d:.2f}")
        else:
            st.latex(rf"s_1 = {s1.real:.2f}, \quad s_2 = {s2.real:.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_s2:
        st.markdown("""
        <div class="math-card">
            <div class="card-label">3. Complex Phasor Voltage Solvation</div>
        """, unsafe_allow_html=True)
        st.latex(rf"\mathbf{{I}} = \frac{{\mathbf{{V}}_{{in}}}}{{\mathbf{{Z}}}} = \frac{{{V_in}\angle 0^\circ}}{{{Z_mag:.2f}\angle {phase_deg:.2f}^\circ}} = {I_rms*1000:.2f}\angle{-phase_deg:.2f}^\circ\,\text{{mA}}")
        st.latex(rf"\mathbf{{V}}_R = \mathbf{{I}} \cdot R = {np.abs(V_R_complex):.2f}\angle{np.degrees(np.angle(V_R_complex)):.2f}^\circ\,\text{{V}}")
        st.latex(rf"\mathbf{{V}}_L = \mathbf{{I}} \cdot jX_L = {np.abs(V_L_complex):.2f}\angle{np.degrees(np.angle(V_L_complex)):.2f}^\circ\,\text{{V}}")
        st.latex(rf"\mathbf{{V}}_C = \mathbf{{I}} \cdot (-jX_C) = {np.abs(V_C_complex):.2f}\angle{np.degrees(np.angle(V_C_complex)):.2f}^\circ\,\text{{V}}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="math-card">
            <div class="card-label">4. Transient Response Closed-Form Solution</div>
        """, unsafe_allow_html=True)
        st.latex(eq_form)
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 🌐 3D Voltage Response Surface V(t)")
        X, Y = np.meshgrid(t, np.linspace(-1, 1, 15))
        Z = np.tile(v_out, (15, 1))

        fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale=colorscale_choice)])
        fig_3d.update_layout(
            scene=dict(
                xaxis=dict(title="Time (s)", backgroundcolor="#0f172a", gridcolor="#334155"),
                yaxis=dict(title="Phase Axis", backgroundcolor="#0f172a", gridcolor="#334155"),
                zaxis=dict(title="Voltage (V)", backgroundcolor="#0f172a", gridcolor="#334155")
            ),
            margin=dict(l=0, r=0, b=0, t=20),
            height=440,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark"
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    with col_right:
        st.markdown("#### 📈 Bode Plot with Bandwidth (-3dB Points)")
        w, mag, phase = signal.bode(sys)
        freq_hz = w / (2 * np.pi)

        fig_bode = go.Figure()
        fig_bode.add_trace(go.Scatter(x=freq_hz, y=mag, mode='lines', name='Magnitude (dB)', line=dict(color='#38bdf8', width=3)))
        
        # Add resonance line & bandwidth region
        fig_bode.add_vline(x=f_0, line_dash="solid", line_color="#FF5252", annotation_text=f"f0 = {f_0:.1f}Hz")
        fig_bode.add_vrect(x0=f_lower, x1=f_upper, fillcolor="rgba(56, 189, 248, 0.15)", line_width=0)
        
        fig_bode.update_layout(
            xaxis=dict(type="log", title="Frequency (Hz)", gridcolor="#334155"),
            yaxis=dict(title="Magnitude (dB)", gridcolor="#334155"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            height=440,
            margin=dict(l=20, r=20, b=20, t=20)
        )
        st.plotly_chart(fig_bode, use_container_width=True)

with tab3:
    st.markdown("### ⚡ Power Triangle & Resonance Parameters")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown("""
        <div class="math-card">
            <div class="card-label">Apparent, Active & Reactive Power Solvation</div>
        """, unsafe_allow_html=True)
        st.write(f"• **Active Power (P):** `{P_real:.3f} Watts` (Real energy dissipated by R)")
        st.write(f"• **Reactive Power (Q):** `{Q_reactive:.3f} VAR` (Energy stored in L and C)")
        st.write(f"• **Apparent Power (|S|):** `{S_apparent:.3f} VA` (Total source power)")
        st.write(f"• **Power Factor (PF):** `{PF:.3f}` ({'Lagging' if X_net > 0 else 'Leading'})")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_p2:
        st.markdown("""
        <div class="math-card">
            <div class="card-label">Resonance & Bandwidth Characteristics</div>
        """, unsafe_allow_html=True)
        st.write(f"• **Resonant Frequency ($f_0$):** `{f_0:.2f} Hz`")
        st.write(f"• **Quality Factor ($Q$):** `{Q_factor:.2f}`")
        st.write(f"• **Passband Bandwidth ($\Delta f$):** `{BW_hz:.2f} Hz`")
        st.write(f"• **Half-Power Frequencies ($f_L, f_U$):** `{f_lower:.1f} Hz` to `{f_upper:.1f} Hz`")
        st.markdown("</div>", unsafe_allow_html=True)