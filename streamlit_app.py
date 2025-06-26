import streamlit as st
import pandas as pd
import numpy as np
from numpy import log, sqrt, exp
import matplotlib.pyplot as plt
import seaborn as sns

#######################
# Page configuration
st.set_page_config(
    page_title="Monte Carlo Option Pricing Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

# Custom CSS styling
st.markdown("""
<style>
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px;
    margin: 0 auto;
}
.metric-call {
    background-color: #90ee90;
    color: black;
    margin-right: 10px;
    border-radius: 10px;
}
.metric-put {
    background-color: #ffcccb;
    color: black;
    border-radius: 10px;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
}
.metric-label {
    font-size: 1rem;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

#######################
# Monte Carlo Class
class MonteCarloOption:
    def __init__(self, S, K, T, r, sigma, simulations=100000):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.simulations = simulations

    def calculate_prices(self):
        np.random.seed(42)
        Z = np.random.standard_normal(self.simulations)
        ST = self.S * np.exp((self.r - 0.5 * self.sigma**2) * self.T + self.sigma * sqrt(self.T) * Z)
        call_payoff = np.maximum(ST - self.K, 0)
        put_payoff = np.maximum(self.K - ST, 0)
        call_price = exp(-self.r * self.T) * np.mean(call_payoff)
        put_price = exp(-self.r * self.T) * np.mean(put_payoff)
        self.call_price = call_price
        self.put_price = put_price
        return call_price, put_price

#######################
# Sidebar for User Inputs
with st.sidebar:
    st.title("📊 Monte Carlo Option Model")
    current_price = st.number_input("Current Asset Price", value=100.0)
    strike = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)
    simulations = st.number_input("Monte Carlo Simulations", value=100000, step=10000)

    st.markdown("---")
    st.markdown("### Heatmap Settings")
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price * 0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price * 1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility * 0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility * 1.5, step=0.01)

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

#######################
# Heatmap Function
def plot_heatmap(T, r, strike, spot_range, vol_range, simulations):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            mc_temp = MonteCarloOption(spot, strike, T, r, vol, simulations)
            call_price, put_price = mc_temp.calculate_prices()
            call_prices[i, j] = call_price
            put_prices[i, j] = put_price

    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                annot=True, fmt=".2f", cmap="YlOrRd", ax=ax_call)
    ax_call.set_title('Call Option Price Heatmap')
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')

    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2),
                annot=True, fmt=".2f", cmap="YlOrRd", ax=ax_put)
    ax_put.set_title('Put Option Price Heatmap')
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')

    return fig_call, fig_put

#######################
# Main Display Area
st.title("Monte Carlo Option Pricing Model")

# Table of Inputs
input_data = {
    "Current Asset Price": [current_price],
    "Strike Price": [strike],
    "Time to Maturity (Years)": [time_to_maturity],
    "Volatility (σ)": [volatility],
    "Risk-Free Interest Rate": [interest_rate],
    "Simulations": [simulations],
}
input_df = pd.DataFrame(input_data)
st.table(input_df)

# Calculate option prices using Monte Carlo
mc_model = MonteCarloOption(current_price, strike, time_to_maturity, interest_rate, volatility, simulations)
call_price, put_price = mc_model.calculate_prices()

# Show results
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">₹{call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">₹{put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Heatmap
st.title("Option Price Heatmaps")
st.info("Explore how option prices change with Spot Price and Volatility.")
fig_call, fig_put = plot_heatmap(time_to_maturity, interest_rate, strike, spot_range, vol_range, simulations)

col1, col2 = st.columns([1, 1])
with col1:
    st.pyplot(fig_call)
with col2:
    st.pyplot(fig_put)
