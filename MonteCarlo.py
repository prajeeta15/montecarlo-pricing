from nsepython import get_optionchain
from math import exp, sqrt
from datetime import datetime, date
import numpy as np
import json
import requests
import nsepython
nsepython.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

# Step 1: Fetch live NIFTY option chain


def fetch_option_chain():
    data = get_optionchain("NIFTY")
    return data


# Step 2: Extract ATM strike and expiry
data = fetch_option_chain()
records = data["records"]
expiry = records["expiryDates"][0]  # nearest expiry
spot = records["underlyingValue"]   # current NIFTY level
# Build list of strikes available
strikes = [item["strikePrice"]
           for item in records["data"] if item["expiryDate"] == expiry]
atm_strike = min(strikes, key=lambda K: abs(K - spot))

# Step 3: Estimate volatility from ATM call IV
atm_data = next(item for item in records["data"]
                if item["expiryDate"] == expiry and item["strikePrice"] == atm_strike)
sigma = atm_data["CE"]["impliedVolatility"] / 100  # convert % to decimal

# Step 4: Compute time to maturity T in years
today = date.today()
expiry_date = datetime.strptime(expiry, "%d-%b-%Y").date()
T = (expiry_date - today).days / 365.0

# Step 5: Risk-free rate – using RBI 10‑yr G‑Sec yield (~7%)
r = 0.07

# Step 6: Monte Carlo simulation


def monte_carlo_price(S, K, T, r, sigma, N=200_000):
    Z = np.random.standard_normal(N)
    ST = S * np.exp((r - 0.5 * sigma**2)*T + sigma * sqrt(T) * Z)
    call = np.exp(-r*T) * np.mean(np.maximum(ST - K, 0))
    put = np.exp(-r*T) * np.mean(np.maximum(K - ST, 0))
    return call, put


call_price, put_price = monte_carlo_price(spot, atm_strike, T, r, sigma)

print(f"NIFTY spot: {spot}")
print(f"Expiry: {expiry_date}, ATM Strike: {atm_strike}")
print(f"Implied vol (ATM): {sigma*100:.2f}%")
print(f"T = {T:.4f} years, r = {r*100:.2f}%")
print(f"→ Monte Carlo Call Price ≈ ₹{call_price:.2f}")
print(f"→ Monte Carlo Put Price ≈ ₹{put_price:.2f}")
