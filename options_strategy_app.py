import streamlit as st
import plotly.graph_objs as go
import numpy as np
from scipy.stats import norm

st.set_page_config(page_title="📊 Option Strategy Analyzer", layout="centered")
st.title("📈 Option Strategy Analyzer with Greeks & Charts")

# Function to calculate option Greeks using Black-Scholes Model
def calculate_greeks(S, K, T_days, r, sigma, option_type='call'):
    T = T_days / 365.0 if T_days > 0 else 0.0001  # prevent divide by zero
    d1 = (np.log(S / K + 1e-9) + (r + sigma ** 2 / 2.) * T) / (sigma * np.sqrt(T) + 1e-9)
    d2 = d1 - sigma * np.sqrt(T)

    delta = norm.cdf(d1) if option_type == 'call' else -norm.cdf(-d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T) + 1e-9)
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))) - r * K * np.exp(-r * T) * norm.cdf(d2)
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100

    return round(delta, 4), round(gamma, 4), round(theta, 4), round(vega, 4)

st.markdown("### 🟢 Enter Option Sentiment Data")

with st.form("input_form"):
    index_choice = st.selectbox("Select Index", ["Nifty", "Nifty Bank", "Sensex"])

    strength = st.number_input("Strength", min_value=0.0, step=0.1)

    vega_sentiment = st.selectbox("Vega", ["Bullish", "Sideways", "Bearish"])
    theta_sentiment = st.selectbox("Theta", ["Bullish", "Sideways", "Bearish"])
    oi_sentiment = st.selectbox("Open Interest (OI)", ["Bullish", "Sideways", "Bearish"])

    st.markdown("### ⚙️ Option Inputs for Greeks (Optional)")
    S = st.number_input("Spot Price (S)", value=0, step=50)
    K = st.number_input("Strike Price (K)", value=0, step=50)
    T_days = st.number_input("Time to Expiry (in days)", value=0)
    r = st.number_input("Risk-free Rate (r, %)", value=10.0) / 100
    sigma = st.number_input("Volatility (VIX, %)", value=10.0) / 100
    option_type = st.selectbox("Option Type", ["call", "put"])
    trade_action = st.selectbox("Trade Action", ["buy", "sell"])

    submitted = st.form_submit_button("🔍 Analyze Strategy")

if submitted:
    if S == 0 or K == 0:
        st.warning("⚠️ Spot price and Strike price must be greater than 0 for Greeks calculation.")
        delta = gamma = theta = vega = 0.0
    else:
        delta, gamma, theta, vega = calculate_greeks(S, K, T_days, r, sigma, option_type)

    st.markdown("### 🔎 Strategy Insights")
    st.write(f"**Index**: {index_choice}")
    st.write(f"**Strength**: {strength}")
    st.write(f"**Vega Sentiment**: {vega_sentiment}")
    st.write(f"**Theta Sentiment**: {theta_sentiment}")
    st.write(f"**Open Interest**: {oi_sentiment}")
    st.write("### 📉 Calculated Greeks")
    st.write(f"**Delta**: {delta}, **Gamma**: {gamma}, **Theta**: {theta}, **Vega**: {vega}")

    st.subheader("🧠 Suggested Strategies")
    if vega_sentiment == "Bullish" and theta_sentiment == "Sideways" and oi_sentiment == "Bullish":
        st.success("📌 Intraday Suggestion: Long Straddle or Bull Call Spread")
        st.info("📌 Positional Suggestion: Long Call or Call Ratio Backspread")
    elif vega_sentiment == "Sideways" and theta_sentiment == "Sideways":
        st.info("📌 Intraday Suggestion: Iron Condor or Calendar Spread")
        st.info("📌 Positional Suggestion: Short Strangle or Delta-Neutral Strategies")
    elif vega_sentiment == "Bullish" and theta_sentiment == "Bullish":
        st.success("📌 Intraday Suggestion: Debit Spread")
        st.success("📌 Positional Suggestion: Long Call, Bull Call Spread, or Synthetic Long")
    elif vega_sentiment == "Bearish" and theta_sentiment == "Bullish" and oi_sentiment == "Bearish":
        st.warning("📌 Intraday Suggestion: Bear Put Spread")
        st.warning("📌 Positional Suggestion: Protective Put or Bear Call Ladder")
    else:
        st.warning("📌 Strategy: Use Delta-Neutral or Risk-defined Spreads for Intraday")
        st.info("📌 Positional Suggestion: Covered Call or Butterfly Spread")

    st.markdown("---")
    st.subheader("💸 PnL Simulation")
    strikes = np.arange(S - 500, S + 500, 50) if S > 0 else np.arange(20000, 26000, 50)
    base_premium = 100
    if trade_action == 'buy':
        pnl = np.maximum(strikes - K, 0) - base_premium if option_type == 'call' else np.maximum(K - strikes, 0) - base_premium
    else:
        pnl = base_premium - np.maximum(strikes - K, 0) if option_type == 'call' else base_premium - np.maximum(K - strikes, 0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strikes, y=pnl, mode='lines', name='PnL'))
    fig.update_layout(title="Payoff Diagram", xaxis_title="Spot Price", yaxis_title="PnL", height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Volatility Smile (Dummy)")
    iv = 20 + 5 * np.sin((strikes - (S if S > 0 else 23000)) / 100)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=strikes, y=iv, mode='lines+markers', name='IV'))
    fig2.update_layout(title="Volatility Smile", xaxis_title="Strike Price", yaxis_title="Implied Volatility", height=400)
    st.plotly_chart(fig2, use_container_width=True)

    st.caption("This is a simulated model. Integrate with live option chain data for accurate Greeks.")
