import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="📊 Options Strategy Wizard", layout="centered")

# ----- Strategy Logic -----
def get_intraday_strategy(strength, vega, theta, oi):
    if strength < 1:
        if vega == "Bullish" and theta == "Bullish":
            return "📈 Buy ATM Call Option (Quick Move Expected)"
        elif vega == "Bullish":
            return "💡 Buy Call Option or Bull Call Spread"
        elif theta == "Bullish":
            return "💰 Sell Put Option or Short Straddle"
        else:
            return "🔍 No Trade / Wait & Watch"
    elif 1 <= strength <= 3:
        if vega == "Bullish":
            return "📊 Buy Call Option / Debit Spread"
        elif theta == "Bullish":
            return "💵 Credit Spread / Sell Puts"
        else:
            return "📦 Iron Condor (Neutral)"
    else:
        if vega == "Bullish":
            return "🚀 Buy Call / Momentum Trade"
        elif theta == "Bullish":
            return "⚡ Short Puts / Scalping"
        else:
            return "🧭 Directional Trade with Tight SL"

def get_positional_strategy(strength, vega, theta, oi):
    if strength > 3 and oi == "Bullish":
        if vega == "Bullish":
            return "🏹 Long Futures + Protective Call / LEAPS"
        elif theta == "Bullish":
            return "🧱 Bull Put Spread / Covered Call"
        else:
            return "📘 Trend-Following via Long Futures"
    elif 1 <= strength <= 3:
        if vega == "Bullish":
            return "💫 Diagonal Call Spread / Buy Call"
        elif theta == "Bullish":
            return "📤 Credit Spread / Put Writing"
        else:
            return "🔐 Straddle / Strangle (Hedged)"
    else:
        if vega == "Bearish" and theta == "Bullish":
            return "🪙 Sell Options (Iron Condor or Strangle)"
        else:
            return "⛔ Avoid Positional Entry - Weak Trend"

# ----- Greeks Calculation -----
def bs_greeks(option_type, S, K, T, r, sigma):
    T = T / 365
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2.) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'Call':
        delta = norm.cdf(d1)
    else:
        delta = -norm.cdf(-d1)

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) -
             r * K * np.exp(-r * T) * norm.cdf(d2 if option_type == 'Call' else -d2)) / 365
    rho = K * T * np.exp(-r * T) * (norm.cdf(d2) if option_type == 'Call' else -norm.cdf(-d2)) / 100
    
    return round(delta,4), round(gamma,4), round(vega,4), round(theta,4), round(rho,4)

# ===== Streamlit UI =====
st.title("📊 OPTIONS STRATEGY WIZARD + GREEKS")

tab1, tab2 = st.tabs(["📈 Strategy Wizard", "📉 Greeks Calculator"])

# --- Tab 1: Strategy Wizard ---
with tab1:
    st.subheader("🎯 Strategy Based on Sentiments")
    index = st.selectbox("Index", ["NIFTY", "BANKNIFTY", "SENSEX"])
    strength = st.number_input("Strength", min_value=0.0, max_value=100.0, step=0.1)
    vega = st.selectbox("Vega Sentiment", ["Bullish", "Sideways", "Bearish"])
    theta = st.selectbox("Theta Sentiment", ["Bullish", "Sideways", "Bearish"])
    oi = st.selectbox("Open Interest (OI)", ["Bullish", "Sideways", "Bearish"])

    if st.button("Suggest Options Strategies"):
        st.subheader("🕒 Intraday Strategy")
        st.success(get_intraday_strategy(strength, vega, theta, oi))

        st.subheader("📅 Positional Strategy")
        st.info(get_positional_strategy(strength, vega, theta, oi))

# --- Tab 2: Option Greeks ---
with tab2:
    st.subheader("🧠 Option Greeks Calculator")

    col1, col2 = st.columns(2)
    with col1:
        option_type = st.selectbox("Option Type", ["Call", "Put"])
        S = st.number_input("Spot Price", value=22000.0)
        K = st.number_input("Strike Price", value=22200.0)
    with col2:
        T = st.number_input("Days to Expiry", value=7)
        sigma = st.number_input("IV (%)", value=20.0) / 100
        r = st.number_input("Risk-free Rate (%)", value=6.0) / 100

    if st.button("Calculate Greeks"):
        delta, gamma, vega, theta, rho = bs_greeks(option_type, S, K, T, r, sigma)
        st.markdown(f"""
        - 📈 **Delta**: `{delta}`
        - 📉 **Gamma**: `{gamma}`
        - 🌊 **Vega**: `{vega}`
        - ⌛ **Theta**: `{theta}`
        - 🏦 **Rho**: `{rho}`
        """)

        # Chart: Delta vs Strike
        strike_range = np.arange(S - 500, S + 500, 50)
        deltas = [bs_greeks(option_type, S, k, T, r, sigma)[0] for k in strike_range]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=strike_range, y=deltas, mode='lines+markers', name='Delta vs Strike'))
        fig.update_layout(title="📊 Delta vs Strike Price", xaxis_title="Strike", yaxis_title="Delta")
        st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("<center><small>Made with ❤️ by Neeraj Bhatia | Streamlit + Python</small></center>", unsafe_allow_html=True)
