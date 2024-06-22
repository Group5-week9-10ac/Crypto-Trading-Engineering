import pandas as pd
import torch
from chronos import ChronosPipeline
import matplotlib.pyplot as plt
import numpy as np

def data_preparation (df):

    # Convert the Date column to datetime and set it as index
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Prepare the context (the Close prices as a torch tensor)
    context = torch.tensor(df["Close"].values, dtype=torch.float32)
    
    return context


def generate_forecast_date(df):
    # Generate forecast dates
    last_date = df.index[-1]
    forecast_dates = pd.date_range(last_date, periods=12 + 1, freq='D')[1:]  # Adjust frequency as needed
    return forecast_dates

def predict(df,forecast_dates,context):
    # Load the pretrained Chronos model
    pipeline = ChronosPipeline.from_pretrained(
    "amazon/chronos-t5-small",
    device_map="cuda",  # use "cpu" for CPU inference and "mps" for Apple Silicon
    torch_dtype=torch.bfloat16,
    )
    # Predict the next 12 time steps with 20 samples for uncertainty estimation
    forecast = pipeline.predict(
        context=context.unsqueeze(0),  # Adding a batch dimension
        prediction_length=12,
        num_samples=20,
    )


    # Extract forecast values and calculate quantiles
    forecast_values = forecast[0].numpy()  # Assuming forecast returns a tensor
    low, median, high = np.percentile(forecast_values, [10, 50, 90], axis=0)

    # Generate forecast dates
    last_date = df.index[-1]
    forecast_dates = pd.date_range(last_date, periods=12 + 1, freq='D')[1:]  # Adjust frequency as needed
    # Print the date range for the forecast
    print("Forecast Dates Range:", forecast_dates[0], "to", forecast_dates[-1])

    # Print the forecast values
    print("Forecast Values (Median):", median)
    print("Forecast Values (Low 10% Quantile):", low)
    print("Forecast Values (High 90% Quantile):", high)

    # Plot the historical data and forecast
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], color="royalblue", label="historical data")
    plt.plot(forecast_dates, median, color="tomato", label="median forecast")
    plt.fill_between(forecast_dates, low, high, color="tomato", alpha=0.3, label="80% prediction interval")
    plt.legend()
    plt.grid()
    plt.xlabel("Date")  # Adding a label to the x-axis
    plt.ylabel("BTC-USD Close Price")  # Adding a label to the y-axis
    plt.title("BTC-USD Close Price Forecast")  # Adding a title to the plot
    plt.show()