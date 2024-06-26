import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';

const Forecast = () => {
    const [coin, setCoin] = useState('BTC');
    const [forecastData, setForecastData] = useState(null);
    const [error, setError] = useState(null);

    const handleCoinChange = (event) => {
        setCoin(event.target.value);
    };

    useEffect(() => {
        axios.get(`http://localhost:5000/forecasts?coin=${coin}`)
            .then(response => {
                setForecastData(response.data);
                setError(null);
            })
            .catch(err => {
                setError(err.message);
                setForecastData(null);
            });
    }, [coin]);

    return (
        <div>
            <h1>{coin}-USD Forecast</h1>
            <select value={coin} onChange={handleCoinChange}>
                <option value="BTC">BTC</option>
                <option value="ETH">ETH</option>
                <option value="BNB">BNB</option>
                <option value="SOL">SOL</option>
                <option value="XRP">XRP</option>
            </select>
            {error ? (
                <p>Error: {error}</p>
            ) : (
                forecastData && (
                    <Plot
                        data={JSON.parse(forecastData).data}
                        layout={JSON.parse(forecastData).layout}
                        config={{ responsive: true }}
                    />
                )
            )}
        </div>
    );
};

export default Forecast;
