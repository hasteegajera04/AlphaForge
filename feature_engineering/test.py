import matplotlib.pyplot as plt

from database.queries import get_stock_dataframe
from feature_engineering.indicators.trend import (
    calculate_ema,
    calculate_hma,
    calculate_sma,
    calculate_wma,
)
from feature_engineering.target import generate_targets

df = get_stock_dataframe("HDFCBANK.NS")

df = calculate_sma(df, 20)
df = calculate_ema(df, 20)
df = calculate_wma(df, 20)
df = calculate_hma(df, 20)

df = generate_targets(df)

print(
    df[
        [
            "close",
            "future_return_5d"
        ]
    ].tail(15)
)

df["future_return_5d"].hist(bins=50)

plt.title("Future Return 5D Distribution")
plt.show()

print(df["future_return_5d"].isna().sum())

df["future_return_5d"].describe()

# ==========================


# Lag Calculation
# ==========================

# df["sma_lag"] = (
#     df["close"] - df["sma_20"]
# ).abs()

# df["ema_lag"] = (
#     df["close"] - df["ema_20"]
# ).abs()

# df["wma_lag"] = (
#     df["close"] - df["wma_20"]
# ).abs()

# df["hma_lag"] = (
#     df["close"] - df["hma_20"]
# ).abs()

# # Remove NaNs created by moving averages
# plot_df = df.dropna().copy()

# # ==========================
# # Plot Comparison
# # ==========================

# plt.figure(figsize=(16, 8))

# plt.plot(
#     plot_df.index,
#     plot_df["close"],
#     label="Close Price",
#     linewidth=1.5
# )

# plt.plot(
#     plot_df.index,
#     plot_df["sma_20"],
#     label="SMA 20",
#     linewidth=0.8
# )

# plt.plot(
#     plot_df.index,
#     plot_df["ema_20"],
#     label="EMA 20",
#     linewidth=0.8
# )

# plt.plot(
#     plot_df.index,
#     plot_df["wma_20"],
#     label="WMA 20",
#     linewidth=0.8
# )

# plt.plot(
#     plot_df.index,
#     plot_df["hma_20"],
#     label="HMA 20",
#     linewidth=0.8
# )

# plt.title(
#     "Close vs SMA vs EMA vs WMA vs HMA"
# )

# plt.xlabel("date")

# plt.ylabel("Price")

# plt.legend()

# plt.grid(True)

# plt.show()

# # ==========================
# # Average Lag Comparison
# # ==========================

# sma_lag = plot_df["sma_lag"].mean()

# ema_lag = plot_df["ema_lag"].mean()

# wma_lag = plot_df["wma_lag"].mean()

# hma_lag = plot_df["hma_lag"].mean()

# print("\nAverage Lag\n")

# print(
#     f"SMA Lag : {sma_lag:.4f}"
# )

# print(
#     f"EMA Lag : {ema_lag:.4f}"
# )

# print(
#     f"WMA Lag : {wma_lag:.4f}"
# )

# print(
#     f"HMA Lag : {hma_lag:.4f}"
# )

# # ==========================
# # Ranking
# # ==========================

# lags = {
#     "SMA": sma_lag,
#     "EMA": ema_lag,
#     "WMA": wma_lag,
#     "HMA": hma_lag
# }

# sorted_lags = sorted(
#     lags.items(),
#     key=lambda x: x[1]
# )

# print("\nLag Ranking (Lower is Better)\n")

# for name, value in sorted_lags:
#     print(
#         f"{name}: {value:.4f}"
#     )