import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Parameters for the Asian option
S0 = st.slider("Initial Stock Price", min_value=85,
               max_value=200, value=100, step=1)      # initial stock price
T = st.slider("Time to Maturity in Years", min_value=0.0,
              max_value=10.0, value=1.0, step=0.01)          # time to maturity in years
r = st.slider("Risk Free Rate", min_value=0.001, max_value=0.05, value=0.02,
              step=0.01)      # risk-free interest rate
sigma = st.slider("Volatility", min_value=0.001, max_value=0.60, value=0.20,
                  step=0.01)   # volatility of the underlying asset
# number of Monte Carlo simulations
n_simulations = st.slider("Number of Simulations",
                          min_value=100, max_value=10000, value=1000, step=100)
# number of steps in the averaging period (daily averaging)
n_steps = st.slider("Number of steps in simulation",
                    min_value=10, max_value=252, value=252, step=1)

# Function to simulate the average price paths


def simulate_average_price_paths(S0, T, r, sigma, n_simulations, n_steps):
    dt = T / n_steps
    price_paths = np.zeros((n_simulations, n_steps))
    average_prices = np.zeros(n_simulations)

    # Simulate price paths
    for i in range(n_simulations):
        prices = [S0]
        for j in range(1, n_steps):
            Z = np.random.normal()
            S_t = prices[j-1] * np.exp((r - 0.5 * sigma**2)
                                       * dt + sigma * np.sqrt(dt) * Z)
            prices.append(S_t)
        price_paths[i] = prices
        average_prices[i] = np.mean(prices)

    return price_paths


price_paths = simulate_average_price_paths(
    S0, T, r, sigma, n_simulations, n_steps)

st.text(f"Length of price paths terminal value is {len(price_paths[:,-1])}")
data = price_paths[:, -1]
fig, ax = plt.subplots()
ax.hist(data, bins=20)

st.pyplot(fig)
