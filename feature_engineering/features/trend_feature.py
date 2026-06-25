def create_trend_features(df):

    # SMA FEATURES

    df["close_div_sma20"] = (df["close"] / df["sma_20"] )
    df["close_div_sma50"] = (df["close"] / df["sma_50"] ) 
    df["close_div_sma200"] = (df["close"] / df["sma_200"] )
    df["sma20_div_sma50"] = (df["sma_20"] / df["sma_50"] )
    df["sma20_div_sma200"] = (df["sma_20"] / df["sma_200"] )
    df["sma50_div_sma200"] = (df["sma_50"] / df["sma_200"] )
    df["sma20_slope"] = (df["sma_20"].diff())
    df["sma50_slope"] = (df["sma_50"].diff())
    df["sma200_slope"] = (df["sma_200"].diff())
    df["price_above_sma200"] = (df["close"] >df["sma_200"]).astype(int)

    # EMA FEATURES

    df["close_div_ema20"] = (df["close"] / df["ema_20"])
    df["close_div_ema50"] = (df["close"] / df["ema_50"])
    df["close_div_ema200"] = (df["close"] / df["ema_200"])
    df["ema20_div_ema50"] = (df["ema_20"] / df["ema_50"])
    df["ema20_div_ema200"] = (df["ema_20"] / df["ema_200"])
    df["ema50_div_ema200"] = (df["ema_50"] / df["ema_200"])
    df["ema20_slope"] = (df["ema_20"].diff())
    df["ema50_slope"] = (df["ema_50"].diff())
    df["ema200_slope"] = (df["ema_200"].diff())
    df["price_above_ema200"] = (df["close"] > df["ema_200"]).astype(int)

    # WMA FEATURES

    df["close_div_wma20"] = (df["close"] / df["wma_20"])
    df["close_div_wma50"] = (df["close"] / df["wma_50"])
    df["close_div_wma200"] = (df["close"] / df["wma_200"])
    df["wma20_div_wma50"] = (df["wma_20"] / df["wma_50"])
    df["wma20_div_wma200"] = (df["wma_20"] / df["wma_200"])
    df["wma50_div_wma200"] = (df["wma_50"] / df["wma_200"])
    df["wma20_slope"] = (df["wma_20"].diff())
    df["wma50_slope"] = (df["wma_50"].diff())
    df["wma200_slope"] = (df["wma_200"].diff())
    df["price_above_wma200"] = (df["close"] > df["wma_200"]).astype(int)

    # HMA FEATURES

    df["close_div_hma20"] = (df["close"] / df["hma_20"])
    df["close_div_hma50"] = (df["close"] / df["hma_50"])
    df["close_div_hma200"] = (df["close"] / df["hma_200"])
    df["hma20_div_hma50"] = (df["hma_20"] / df["hma_50"])
    df["hma20_div_hma200"] = (df["hma_20"] / df["hma_200"])
    df["hma50_div_hma200"] = (df["hma_50"] / df["hma_200"])
    df["hma20_slope"] = (df["hma_20"].diff())
    df["hma50_slope"] = (df["hma_50"].diff())
    df["hma200_slope"] = (df["hma_200"].diff())
    
    return df
    
