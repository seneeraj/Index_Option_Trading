import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="📊 Options Strategy Pro", layout="centered")

# ======= STRATEGY DECISION LOGIC =======
def suggest_strategy(iv, spot, strike_diff, theta, vega):
    if iv > 0.3:
        if theta > 0:
            return "🔹 Short Straddle or Short Strangle"
        else:
            return "🔹 Long Butterfly or Iron Condor"
    elif iv < 0.15:
        if vega > 0:
            return "🔹 Long Straddle or Long Call"
        else:
            return "🔹 Debit Spread or Calendar Spread"
    else:
        if abs(strike_diff) <= 200:
            return "🔹 Iron Fly or Short Iron Condor"
        else:
            return "🔹 Bull Call Spread or Bear Put Spread"

# ======= STREAMLIT UI =======
st.title("🧠 Options Strategy Pro")

col1, col2 = st.columns(2)
with col1:
    iv = st.number_input("IV (Implied Volatility)", value=0.25, step=0.01)
    spot = st.number_input("Spot Price", value=22000.0)
    strike_price = st.number_input("Strike Price", value=22200.0)
    contracts = st.number_input("Lot Size (Qty)", value=50)
with col2:
    theta = st.number_input("Theta", value=-5.0, step=0.1)
    vega = st.number_input("Vega", value=15.0, step=0.1)
    delta = st.number_input("Delta", value=0.6, step=0.01)
    gamma = st.number_input("Gamma", value=0.05, step=0.01)

if st.button("🔍 Suggest Best Strategy"):
    strike_diff = strike_price - spot
    strategy = suggest_strategy(iv, spot, strike_diff, theta, vega)

    st.markdown(f"""
    ### 📌 Strategy Suggestion
    - **📍 IV**: `{iv}`
    - **📉 Theta**: `{theta}`
    - **📈 Vega**: `{vega}`
    - **⚡ Delta**: `{delta}`
    - **🎯 Gamma**: `{gamma}`
    - **💡 Suggested Strategy**: `{strategy}`
    """)

    # ===== PNL Simulation =====
    price_range = np.linspace(spot * 0.9, spot * 1.1, 50)
    pnl = []
    for s in price_range:
        move = (s - strike_price)
        premium = vega * (iv * 100) - theta
        payoff = move - premium if delta > 0 else -move - premium
        pnl.append(payoff * contracts)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=price_range, y=pnl, mode='lines', name='PnL'))
    fig1.update_layout(title="💹 PnL Simulation at Expiry", xaxis_title="Underlying Price", yaxis_title="PnL (₹)")
    st.plotly_chart(fig1, use_container_width=True)

    # ===== Volatility Smile =====
    strike_range = np.arange(spot - 1000, spot + 1000, 100)
    ivs = []
    for k in strike_range:
        imp_vol = iv + 0.02 * np.abs(k - spot) / spot  # Simple smile logic
        ivs.append(imp_vol * 100)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=strike_range, y=ivs, mode='lines+markers', name='IV Smile'))
    fig2.update_layout(title="😊 Volatility Smile", xaxis_title="Strike Price", yaxis_title="Implied Volatility (%)")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.markdown("<center><small>Advanced Options App by Neeraj Bhatia</small></center>", unsafe_allow_html=True)
