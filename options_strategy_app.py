import streamlit as st
import plotly.graph_objs as go
import numpy as np

st.set_page_config(page_title="📊 Option Strategy Analyzer", layout="centered")
st.title("📈 Option Strategy Analyzer with Greeks & Charts")

st.markdown("### 🟢 Enter Option Sentiment Data")

with st.form("input_form"):
    col1 = st.columns(1)[0]
    strength = col1.number_input("Strength", min_value=0.0, step=0.1)

    col2, col3, col4 = st.columns(3)
    with col2:
        vega = st.selectbox("Vega", ["Bullish", "Sideways", "Bearish"])
    with col3:
        theta = st.selectbox("Theta", ["Bullish", "Sideways", "Bearish"])
    with col4:
        oi = st.selectbox("Open Interest (OI)", ["Bullish", "Sideways", "Bearish"])

    st.markdown("### ⚙️ Option Greeks")
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        delta = st.slider("Delta", -1.0, 1.0, 0.5)
    with col6:
        gamma = st.slider("Gamma", 0.0, 1.0, 0.1)
    with col7:
        theta_greek = st.slider("Theta (Greek)", -10.0, 0.0, -2.0)
    with col8:
        vega_greek = st.slider("Vega (Greek)", 0.0, 2.0, 0.5)

    submitted = st.form_submit_button("🔍 Analyze Strategy")

if submitted:
    st.markdown("### 🔎 Strategy Insights")
    st.write(f"**Strength**: {strength}")
    st.write(f"**Vega**: {vega}")
    st.write(f"**Theta**: {theta}")
    st.write(f"**Open Interest**: {oi}")

    if vega == "Bullish" and theta == "Sideways" and oi == "Bullish":
        st.success("📌 Intraday Suggestion: Long Straddle or Bull Call Spread")
    elif vega == "Sideways" and theta == "Sideways":
        st.info("📌 Intraday Suggestion: Iron Condor or Calendar Spread")
    elif vega == "Bullish" and theta == "Bullish":
        st.success("📌 Positional Strategy: Debit Spread or Long Call")
    else:
        st.warning("📌 Strategy: Use Delta-Neutral or Risk-defined Spreads")

    st.markdown("---")
    st.subheader("💸 PnL Simulation")
    cmp = 24000  # Default CMP for payoff simulation
    strikes = np.arange(cmp - 500, cmp + 500, 50)
    pnl = np.maximum(strikes - cmp, 0) - 100  # Simplified payoff
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strikes, y=pnl, mode='lines', name='PnL'))
    fig.update_layout(title="Payoff Diagram", xaxis_title="Spot Price", yaxis_title="PnL", height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Volatility Smile (Dummy)")
    iv = 20 + 5 * np.sin((strikes - cmp) / 100)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=strikes, y=iv, mode='lines+markers', name='IV'))
    fig2.update_layout(title="Volatility Smile", xaxis_title="Strike Price", yaxis_title="Implied Volatility", height=400)
    st.plotly_chart(fig2, use_container_width=True)

    st.caption("This is a simplified simulation. Use live data for real strategies.")
