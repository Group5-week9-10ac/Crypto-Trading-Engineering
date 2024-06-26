import torch
import matplotlib.pyplot as plt
import pandas as pd
from gluonts.dataset.pandas import PandasDataset
from gluonts.dataset.split import split
from uni2ts.eval_util.plot import plot_single
from uni2ts.model.moirai import MoiraiForecast, MoiraiModule
import plotly.graph_objs as go

# Function to plot a single time series with forecast and ground truth
def plot_single_interactive(input_data, label_data, forecast_data, context_length, name="pred", show_label=True):
    # Check if 'time' key is present in input_data
    if 'time' in input_data:
        time_idx = pd.date_range(start=input_data["time"][0], periods=len(input_data["target"]) + len(forecast_data.samples[0]), freq="D")
    else:
        time_idx = pd.date_range(start="2024-01-01", periods=len(input_data["target"]) + len(forecast_data.samples[0]), freq="D")  # Replace with appropriate start date
    
    # Plotting observed data
    trace_observed = go.Scatter(
        x=time_idx[:len(input_data["target"])],
        y=input_data["target"],
        mode="lines+markers",
        name="Observed",
        line=dict(color='blue'),
    )
    
    # Plotting ground truth data if available
    if label_data is not None:
        trace_label = go.Scatter(
            x=time_idx[len(input_data["target"]):],
            y=label_data["target"],
            mode="lines+markers",
            name="Ground Truth",
            line=dict(color='green'),
        )
    else:
        trace_label = None
    
    # Plotting forecasted data
    trace_forecast = go.Scatter(
        x=time_idx[len(input_data["target"]):],
        y=forecast_data.samples[0],
        mode="lines+markers",
        name="Forecast",
        line=dict(color='red'),
    )
    
    # Create plot data list
    plot_data = [trace_observed]
    if trace_label:
        plot_data.append(trace_label)
    plot_data.append(trace_forecast)
    
    # Create layout
    layout = go.Layout(
        title="Interactive Forecast Plot",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Value"),
        hovermode='closest'
    )
    
    # Create figure and plot
    fig = go.Figure(data=plot_data, layout=layout)
    fig.show()

def moirai_forecast(df):
    # Ensure the 'Date' column is in datetime format and set it as index
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    SIZE = "small"  # model size: choose from {'small', 'base', 'large'}
    PDT = 20  # prediction length: any positive integer
    CTX = 200  # context length: any positive integer
    PSZ = "auto"  # patch size: choose from {"auto", 8, 16, 32, 64, 128}
    BSZ = 32  # batch size: any positive integer
    TEST = 100  # test set length: any positive integer

    # Convert into GluonTS dataset
    target_column = df['close']  # Use the 'close' column as the target
    df_gluon = df[['close']]  # Create a DataFrame with only the target column for GluonTS
    ds = PandasDataset(dict(df_gluon), target='close')

    # Parameters
    PDT = 20  # prediction length
    CTX = 200  # context length
    PSZ = "auto"  # patch size
    BSZ = 32  # batch size
    TEST = 100  # test set length

    # Split into train/test set
    train, test_template = split(ds, offset=-TEST)

    # Construct rolling window evaluation
    test_data = test_template.generate_instances(
        prediction_length=PDT,
        windows=TEST // PDT,
        distance=PDT,
    )

    # Prepare pre-trained model
    model = MoiraiForecast(
        module=MoiraiModule.from_pretrained(f"Salesforce/moirai-1.0-R-{SIZE}"),
        prediction_length=PDT,
        context_length=CTX,
        patch_size=PSZ,
        num_samples=100,
        target_dim=1,
        feat_dynamic_real_dim=ds.num_feat_dynamic_real,
        past_feat_dynamic_real_dim=ds.num_past_feat_dynamic_real,
    )

    # Create predictor and generate forecasts
    predictor = model.create_predictor(batch_size=BSZ)
    forecasts = predictor.predict(test_data.input)

    # Extract data for plotting
    input_it = iter(test_data.input)
    label_it = iter(test_data.label)
    forecast_it = iter(forecasts)

    inp = next(input_it)
    label = next(label_it, None)  # Handling case where label may be None
    forecast = next(forecast_it)

    # Plot using Plotly interactive plot function
    plot_single_interactive(inp, label, forecast, context_length=CTX, name="pred", show_label=True)