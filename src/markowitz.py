import duckdb
import pandas as pd
import numpy as np
from scipy.optimize import minimize

# ── Step 1: Export returns from DuckDB (read-only) ────────────────────────────
print("Step 1: Reading data from DuckDB...")
conn = duckdb.connect("stock_market_duckdb.db", read_only=True)

df = conn.execute("""
    SELECT date, ticker,
           ROUND((close - open) / NULLIF(open, 0) * 100, 6) AS daily_return
    FROM fact_stock_prices
    WHERE open > 0
    ORDER BY ticker, date
""").df()
conn.close()

# ── Step 2: Pivot to returns matrix ───────────────────────────────────────────
print("Step 2: Building returns matrix...")
returns = df.pivot(index="date", columns="ticker", values="daily_return").dropna()
print(f"  Shape: {returns.shape[0]} trading days x {returns.shape[1]} tickers")

# Export CSV so original project stays untouched
returns.to_csv("data/markowitz_returns.csv")
print("  Exported to data/markowitz_returns.csv")

# ── Step 3: Compute covariance matrix and mean returns ────────────────────────
print("Step 3: Computing covariance matrix...")
mu = returns.mean().values          # mean daily returns
cov = returns.cov().values          # covariance matrix
n = len(mu)
print(f"  {n} assets")

# ── Step 4: Equal-weighted baseline ───────────────────────────────────────────
print("\nStep 4: Equal-weighted baseline...")
w_equal = np.ones(n) / n
var_equal = w_equal @ cov @ w_equal
ret_equal = w_equal @ mu
sharpe_equal = (ret_equal / np.sqrt(var_equal)) * np.sqrt(252)

print(f"  Equal-weight variance  : {var_equal:.6f}")
print(f"  Equal-weight return    : {ret_equal:.6f}%/day")
print(f"  Equal-weight Sharpe    : {sharpe_equal:.4f}")

# ── Step 5: Markowitz minimum variance optimisation ───────────────────────────
print("\nStep 5: Running Markowitz optimisation (scipy.optimize / SLSQP)...")

def portfolio_variance(w):
    return w @ cov @ w

constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
bounds = [(0, 1)] * n
w0 = np.ones(n) / n

result = minimize(
    portfolio_variance,
    w0,
    method="SLSQP",
    bounds=bounds,
    constraints=constraints,
    options={"ftol": 1e-12, "maxiter": 1000}
)

if not result.success:
    print(f"  WARNING: solver did not converge — {result.message}")
else:
    print(f"  Solver: scipy.optimize / SLSQP")
    print(f"  Converged: {result.success}")

w_opt = result.x
var_opt = portfolio_variance(w_opt)
ret_opt = w_opt @ mu
sharpe_opt = (ret_opt / np.sqrt(var_opt)) * np.sqrt(252)

# ── Step 6: Results ───────────────────────────────────────────────────────────
variance_reduction = (var_equal - var_opt) / var_equal * 100

print("\n" + "=" * 55)
print("  MARKOWITZ OPTIMISATION RESULTS")
print("=" * 55)
print(f"  Solver                    : scipy.optimize / SLSQP")
print(f"  Assets                    : {n}")
print(f"  Trading days              : {returns.shape[0]}")
print()
print(f"  Equal-weight variance     : {var_equal:.6f}")
print(f"  Optimised variance        : {var_opt:.6f}")
print(f"  Variance reduction        : {variance_reduction:.2f}%")
print()
print(f"  Equal-weight Sharpe ratio : {sharpe_equal:.4f}")
print(f"  Optimised Sharpe ratio    : {sharpe_opt:.4f}")
print()
print("  Top 5 optimal weights:")
tickers = returns.columns.tolist()
weights_df = pd.DataFrame({"ticker": tickers, "weight": w_opt})
weights_df = weights_df.sort_values("weight", ascending=False)
for _, row in weights_df.head(5).iterrows():
    print(f"    {row['ticker']:<20} {row['weight']*100:.2f}%")

print()
weights_df.to_csv("data/markowitz_weights.csv", index=False)
print("  Weights exported to data/markowitz_weights.csv")