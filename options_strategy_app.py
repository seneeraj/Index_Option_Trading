import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain

# --- Page Setup ---
st.set_page_config(page_title="📊 Options Strategy Wizard", layout="centered")

st.markdown("""
    <style>
        .stSelectbox > div > div {
            font-size: 16px !important;
        }
        .stNumberInput > div > div {
            font-size: 16px !important;
        }
        .stButton > button {
            background-color: #0A75AD;
            color: white;
            font-weight: bold;
            width: 100%;
        }
        .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Strategy Logic ---
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

# --- Main App UI ---
colored_header(label="📊 OPTIONS STRATEGY WIZARD", description="Get best Intraday & Positional strategy based on market sentiment", color_name="blue-70")

index = st.selectbox("📍 Select Index", ["NIFTY", "BANKNIFTY", "SENSEX"])
strength = st.number_input("📊 Enter Strength", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")
vega = st.selectbox("🧠 Vega Sentiment", ["Bullish", "Sideways", "Bearish"])
theta = st.selectbox("⌛ Theta Sentiment", ["Bullish", "Sideways", "Bearish"])
oi = st.selectbox("📦 Open Interest (OI)", ["Bullish", "Sideways", "Bearish"])

if st.button("🎯 Suggest Strategies"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🕒 Intraday Strategy")
        st.success(get_intraday_strategy(strength, vega, theta, oi))
    with col2:
        st.markdown("### 🏛️ Positional Strategy")
        st.info(get_positional_strategy(strength, vega, theta, oi))

    rain(emoji="📈", font_size=25, falling_speed=5, animation_length="infinite")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<center><small>Made with ❤️ by Neeraj Bhatia | Powered by Streamlit</small></center>",
    unsafe_allow_html=True
)
