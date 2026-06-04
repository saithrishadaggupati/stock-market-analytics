import duckdb
import pandas as pd
from scipy import stats

# ── connect ────────────────────────────────────────────────────────────────────
conn = duckdb.connect("stock_market_duckdb.db", read_only=True)

def get_daily_returns(sector):
    return conn.execute("""
        SELECT ticker, sector,
               ROUND((close - open) / NULLIF(open, 0) * 100, 4) AS daily_pct_change
        FROM fact_stock_prices
        WHERE sector = ? AND open > 0
    """, [sector]).df()["daily_pct_change"].dropna().values


def run_test(label, sector_a, sector_b):
    a = get_daily_returns(sector_a)
    b = get_daily_returns(sector_b)

    t_stat, p_value = stats.ttest_ind(a, b, equal_var=False)  # Welch's t-test

    mean_a = round(a.mean(), 4)
    mean_b = round(b.mean(), 4)
    significant = p_value < 0.05

    print(f"\n{'─' * 55}")
    print(f"  TEST: {label}")
    print(f"{'─' * 55}")
    print(f"  {sector_a:<12}  mean daily return = {mean_a:>8}%  (n={len(a):,})")
    print(f"  {sector_b:<12}  mean daily return = {mean_b:>8}%  (n={len(b):,})")
    print(f"  t-statistic = {round(t_stat, 4)},  p-value = {round(p_value, 6)}")

    if significant:
        winner = sector_a if mean_a > mean_b else sector_b
        print(f"  ✅ Statistically significant (p < 0.05)")
        print(f"     → {winner} outperforms with higher average daily return")
    else:
        print(f"  ❌ Not statistically significant (p ≥ 0.05)")
        print(f"     → No reliable performance difference between the two sectors")

    return {
        "test": label,
        "sector_a": sector_a,
        "sector_b": sector_b,
        "mean_a": mean_a,
        "mean_b": mean_b,
        "t_stat": round(t_stat, 4),
        "p_value": round(p_value, 6),
        "significant": significant,
    }


# ── run three tests ────────────────────────────────────────────────────────────
print("\n📊 A/B Testing — Sector Return Comparisons")
print("   Hypothesis: sectors differ in mean daily return")
print("   Method: Welch's independent samples t-test (α = 0.05)")

results = []
results.append(run_test("US Tech vs Indian IT",      "Tech",    "IT"))
results.append(run_test("Tech vs Other",             "Tech",    "Other"))
results.append(run_test("Indian IT vs Banking",      "IT",      "Banking"))

# ── summary table ──────────────────────────────────────────────────────────────
print(f"\n\n{'═' * 55}")
print("  SUMMARY")
print(f"{'═' * 55}")
df = pd.DataFrame(results)[["test", "mean_a", "mean_b", "p_value", "significant"]]
df.columns = ["Test", "Mean A (%)", "Mean B (%)", "p-value", "Significant"]
print(df.to_string(index=False))

conn.close()