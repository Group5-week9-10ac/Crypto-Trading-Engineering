import pandas as pd
import torch
from chronos import ChronosPipeline
import plotly.graph_objs as go
import numpy as np

def data_preparation(df):
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    context = torch.tensor(df["close"].values, dtype=torch.float32)
    return context

def generate_forecast_dates(df):
    last_date = df.index[-1]
    forecast_dates = pd.date_range(last_date, periods=12 + 1, freq='D')[1:]
    return forecast_dates

def predict(name, df, forecast_dates, context):
    pipeline = ChronosPipeline.from_pretrained(
        "amazon/chronos-t5-small",
        device_map="cpu",
        torch_dtype=torch.float32,
    )
    forecast = pipeline.predict(
        context=context.unsqueeze(0),
        prediction_length=12,
        num_samples=20,
    )
    forecast_values = forecast[0].cpu().numpy()
    low, median, high = np.percentile(forecast_values, [10, 50, 90], axis=0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["close"], mode='lines', name='Historical Data'))
    fig.add_trace(go.Scatter(x=forecast_dates, y=median, mode='lines', name='Forecast'))
    fig.add_trace(go.Scatter(x=forecast_dates, y=low, fill=None, mode='lines', line_color='lightgray', showlegend=False))
    fig.add_trace(go.Scatter(x=forecast_dates, y=high, fill='tonexty', mode='lines', line_color='lightgray', showlegend=False))

    fig.update_layout(title=f"{name}-USD Close Price Forecast", xaxis_title="Date", yaxis_title="Price")

    return fig
