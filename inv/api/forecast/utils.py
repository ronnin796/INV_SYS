from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np

def forecast_sales_for_product(product, warehouse, sales_qs, days_ahead=30):
    """
    Takes in sales queryset and returns forecast stats (including debug info).
    """
    if not sales_qs.exists():
        print(f"[DEBUG] No sales found for {product.name} in {warehouse.name}")
        return None

    # Convert sales queryset to DataFrame
    df = pd.DataFrame.from_records(sales_qs.values("created_at", "quantity"))
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # Group by date and sum quantities
    df = df.groupby(df["created_at"].dt.date)["quantity"].sum()
    df = df.astype(float)

    # ✅ Debug info: check if data is loaded properly
    print(f"\n=== DEBUG: Sales Data for {product.name} @ {warehouse.name} ===")
    print(df.head(10))
    print(f"Total records: {len(df)} | Date Range: {df.index.min()} → {df.index.max()}")

    if len(df) < 3:  # Avoid ARIMA crash on tiny data
        print(f"[DEBUG] Not enough records for ARIMA ({len(df)} found)")
        return None

    try:
        model = ARIMA(df, order=(1, 1, 1))
        fitted = model.fit()

        forecast_series = fitted.forecast(steps=days_ahead)
        forecast_dates = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=days_ahead)

        # ✅ Debug forecast info
        print("\n=== DEBUG: Forecast Output ===")
        print(f"Forecast Dates: {forecast_dates.min().date()} → {forecast_dates.max().date()}")
        print(f"Forecasted Values (first 5): {forecast_series.head().tolist()}")

    except Exception as e:
        print(f"[ERROR] ARIMA failed for {product.name}: {e}")
        return None

    return {
        # For visualizations
        "historical": {str(date): float(val) for date, val in zip(df.index, df.values)},
        "forecast": {str(date.date()): float(val) for date, val in zip(forecast_dates, forecast_series)},
        "forecast_series": list(map(float, forecast_series)),
        "predicted_total_sales": float(forecast_series.sum())
    }
