import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from utils import preprocess_data, create_sequences, inverse_transform
from lstm_model import build_lstm_model
from config import DATA_FILE, MODEL_FILE, SEQUENCE_LENGTH, EPOCHS, BATCH_SIZE

# Load data
data = pd.read_csv(DATA_FILE)

# Prepare the dataset
data = data[['Close']].dropna()
scaler, scaled_data = preprocess_data(data)

# Split the data into training and testing sets
train_size = int(len(scaled_data) * 0.8)
train_data, test_data = scaled_data[:train_size], scaled_data[train_size:]

# Create sequences for LSTM
X_train, y_train = create_sequences(train_data, SEQUENCE_LENGTH)
X_test, y_test = create_sequences(test_data, SEQUENCE_LENGTH)

# Reshape data for LSTM [samples, time steps, features]
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Build the LSTM model
model = build_lstm_model(SEQUENCE_LENGTH)

# Train the model
history = model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(X_test, y_test))

# Predict the test data
predicted_prices = model.predict(X_test)
predicted_prices = inverse_transform(scaler, predicted_prices)

# Inverse transform the actual prices
actual_prices = inverse_transform(scaler, y_test)

# Calculate RMSE (Root Mean Squared Error)
rmse = np.sqrt(mean_squared_error(actual_prices, predicted_prices))
print(f"Root Mean Squared Error: {rmse}")

# Plot the results
plt.figure(figsize=(14, 8))
plt.plot(actual_prices, label='Actual Prices')
plt.plot(predicted_prices, label='Predicted Prices')
plt.title('Actual vs Predicted Prices')
plt.xlabel('Time')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Save the model
model.save(MODEL_FILE)
print(f"Model saved to {MODEL_FILE}")
