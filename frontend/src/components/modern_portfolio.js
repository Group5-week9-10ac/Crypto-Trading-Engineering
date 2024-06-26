import React, { useState, useEffect } from 'react';
import './ModernPortfolio.css'; // External CSS for styling
import LoadingSpinner from './LoadingSpinner'; // Import LoadingSpinner component

function ModernPortfolio() {
    const [portfolioData, setPortfolioData] = useState(null);
    const [lowRiskData, setLowRiskData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPortfolioData = async () => {
            try {
                const res = await fetch("http://localhost:5000/results");
                if (!res.ok) {
                    const text = await res.text();
                    throw new Error(`HTTP error! Status: ${res.status}, Message: ${text}`);
                }
                const data = await res.json();
                setPortfolioData(data);
            } catch (error) {
                setError(error);
            }
        };

        const fetchLowRiskData = async () => {
            try {
                const res = await fetch("http://localhost:5000/results2");
                if (!res.ok) {
                    const text = await res.text();
                    throw new Error(`HTTP error! Status: ${res.status}, Message: ${text}`);
                }
                const data = await res.json();
                setLowRiskData(data);
            } catch (error) {
                setError(error);
            }
        };

        const fetchData = async () => {
            setLoading(true);
            await fetchPortfolioData();
            await fetchLowRiskData();
            setLoading(false);
        };

        fetchData();
    }, []);

    if (loading) {
        return <LoadingSpinner />; // Use a spinner instead of text
    }

    if (error) {
        return <p className="error">Error: {error.message}</p>;
    }

    return (
        <div className="portfolio-container">
            <h1 className="title">Modern Portfolio</h1>
            {portfolioData ? (
                <div className="data-container">
                    <h2>High Sharp Ratio Portfolio</h2>
                    <p><strong>Annual Volatility:</strong> {portfolioData.annual_volatility}</p>
                    <p><strong>Expected Return:</strong> {portfolioData.expected_return}</p>
                    <p><strong>Sharpe Ratio:</strong> {portfolioData.sharpe_ratio}</p>
                    <h4>Weights:</h4>
                    <ul>
                        {Object.entries(portfolioData.weights).map(([key, value]) => (
                            <li key={key}><strong>{key}:</strong> {value}</li>
                        ))}
                    </ul>
                </div>
            ) : (
                <p>No portfolio data available.</p>
            )}
            {lowRiskData ? (
                <div className="data-container">
                    <h2>Low Risk Portfolio</h2>
                    <p><strong>Annual Volatility:</strong> {lowRiskData.annual_volatility}</p>
                    <p><strong>Expected Return:</strong> {lowRiskData.expected_return}</p>
                    <p><strong>Sharpe Ratio:</strong> {lowRiskData.sharpe_ratio}</p>
                    <h4>Weights:</h4>
                    <ul>
                        {Object.entries(lowRiskData.weights).map(([key, value]) => (
                            <li key={key}><strong>{key}:</strong> {value}</li>
                        ))}
                    </ul>
                </div>
            ) : (
                <p>No low risk portfolio data available.</p>
            )}
        </div>
    );
}

export default ModernPortfolio;
