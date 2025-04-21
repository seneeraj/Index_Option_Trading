import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="📊 Options Strategy Pro", layout="centered")

# ======= BLACK SCHOLES CALCULATION =======
def bs_price(option_type, S, K, T, r, sigma):
    T = T / 365
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2.) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'Call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

def bs_greeks(option_type, S, K, T, r, sigma):
    T = T / 365
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2.) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    delta = norm.cdf(d1) if option_type == 'Call' else -norm.cdf(-d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) -
             r * K * np.exp(-r * T) * norm.cdf(d2 if option_type == 'Call' else -d2)) / 365
    rho = K * T * np.exp(-r * T) * (norm.cdf(d2) if option_type == 'Call' else -norm.cdf(-d2)) / 100
    return round(delta,4), round(gamma,4), round(vega,4), round(theta,4), round(rho,4)

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
    option_type = st.selectbox("Option Type", ["Call", "Put"])
    S = st.number_input("Spot Price", value=22000.0)
    K = st.number_input("Strike Price", value=22200.0)
    T = st.number_input("Days to Expiry", value=7)
with col2:
    sigma = st.number_input("IV (%)", value=20.0) / 100
    r = st.number_input("Risk-free Rate (%)", value=6.0) / 100
    contracts = st.number_input("Lot Size (Qty)", value=50)

if st.button("🧮 Calculate & Simulate"):
    # Greeks
    delta, gamma, vega, theta, rho = bs_greeks(option_type, S, K, T, r, sigma)
    price = bs_price(option_type, S, K, T, r, sigma)
    strategy = suggest_strategy(sigma, S, K - S, theta, vega)

    st.markdown(f"""
    ### 📊 Option Metrics
    - **Premium**: `{round(price,2)}`
    - **Delta**: `{delta}`
    - **Gamma**: `{gamma}`
    - **Vega**: `{vega}`
    - **Theta**: `{theta}`
    - **Rho**: `{rho}`
    - **📌 Suggested Strategy**: `{strategy}`
    """)

    # ===== PNL Simulation =====
    price_range = np.linspace(S * 0.9, S * 1.1, 50)
    pnl = []
    for s in price_range:
        payoff = bs_price(option_type, s, K, T, r, sigma) - price
        pnl.append(payoff * contracts)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=price_range, y=pnl, mode='lines', name='PnL'))
    fig1.update_layout(title="💹 PnL Simulation at Expiry", xaxis_title="Underlying Price", yaxis_title="PnL (₹)")
    st.plotly_chart(fig1, use_container_width=True)

    # ===== Volatility Smile =====
    strike_range = np.arange(S - 1000, S + 1000, 100)
    ivs = []
    for k in strike_range:
        imp_vol = sigma + 0.02 * np.abs(k - S) / S  # Simple smile logic
        ivs.append(imp_vol * 100)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=strike_range, y=ivs, mode='lines+markers', name='IV Smile'))
    fig2.update_layout(title="😊 Volatility Smile", xaxis_title="Strike Price", yaxis_title="Implied Volatility (%)")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.markdown("<center><small>Advanced Options App by Neeraj Bhatia</small></center>", unsafe_allow_html=True)
