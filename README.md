This repository contains an interactive Streamlit dashboard that uses a Monte Carlo simulation to estimate the prices of European Call and Put options. Unlike the closed-form Black-Scholes formula, this model provides a probabilistic estimate by simulating multiple possible future asset price paths.

🔗 Live Demo: https://montecarlo-pricing.streamlit.app/

## 🚀 Features

### 1. 🎯 Monte Carlo Simulation for Options Pricing
- Simulates thousands of possible asset price paths.
- Calculates expected Call and Put option prices based on payoff distributions.
- Provides a probabilistic estimate more suitable for less ideal/efficient markets (like the Indian options market).

### 2. 📊 Interactive Heatmaps
- Real-time heatmap generation for Call and Put prices.
- Visualizes how option prices vary with different:
  - Spot Prices
  - Volatility levels
  - Strike Price
  - Time to Maturity
  - Interest Rates

### 3. ⚙️ Customizable Input Parameters
- Modify key financial parameters using sliders or inputs in the sidebar.
- Compare Call vs. Put prices side-by-side in a visually enhanced dashboard.

---

## 📦 Requirements

To run locally, install the dependencies:

```bash
pip install -r requirements.txt
