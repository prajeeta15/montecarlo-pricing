# 🧮 Monte Carlo Option Pricing Model

This repository hosts an interactive **Monte Carlo-based Option Pricing Dashboard** built using Streamlit. It allows users to visualize how **Call and Put options** behave under different market conditions using a simulation-based approach rather than a closed-form Black-Scholes formula.

🔗 **Live App**: [https://montecarlo-pricing.streamlit.app/](https://montecarlo-pricing.streamlit.app/)  

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

### 4. 🌐 Built with Streamlit
- Responsive and clean UI.
- Easy to deploy via [Streamlit Community Cloud](https://streamlit.io/cloud).

---

## 📦 Requirements

To run locally, install the dependencies:

```bash
pip install -r requirements.txt
