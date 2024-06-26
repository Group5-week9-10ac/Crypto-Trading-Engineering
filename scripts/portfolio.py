from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

def lowrisk_porfolio(df):
    mu = expected_returns.mean_historical_return(df)
    sigma = risk_models.sample_cov(df)

    # Create an Efficient Frontier object
    ef_low_risk = EfficientFrontier(mu, sigma)

    # Optimize for the minimum volatility
    weights_low_risk = ef_low_risk.min_volatility()

    # Clean the weights
    cleaned_weights_low_risk = ef_low_risk.clean_weights()

    # Display the optimized weights
    print("Weights for Lowest Risk Portfolio:")
    print(cleaned_weights_low_risk)
    # Portfolio performance
    performance_low_risk = ef_low_risk.portfolio_performance(verbose=True)
    
    expected_return = performance_low_risk[0] * 100  # Converting to percentage
    annual_volatility = performance_low_risk[1] * 100  # Converting to percentage
    sharpe_ratio = performance_low_risk[2]
    expected_return =f'{round(expected_return, ndigits=0)}%'
    annual_volatility =f'{round(annual_volatility, ndigits=0)}%'
    sharpe_ratio =f'{round(sharpe_ratio, ndigits=0)}%'

    return {
        "weights": cleaned_weights_low_risk ,
        "expected_return": expected_return,
        "annual_volatility": annual_volatility,
        "sharpe_ratio": sharpe_ratio
    }

def ef_portfolio(df):
    mu = expected_returns.mean_historical_return(df)
    sigma = risk_models.sample_cov(df)
    
    # Create an Efficient Frontier object
    ef_high_sharpe = EfficientFrontier(mu, sigma)
    
    # Optimize for the maximal Sharpe ratio
    weights_high_sharpe = ef_high_sharpe.max_sharpe()
    
    # Clean the weights
    cleaned_weights_high_sharpe = ef_high_sharpe.clean_weights()
    
    # Portfolio performance
    performance_high_sharpe = ef_high_sharpe.portfolio_performance(verbose=False)
    
    # Format the performance metrics
    
    expected_return = performance_high_sharpe[0] * 100  # Converting to percentage
    annual_volatility = performance_high_sharpe[1] * 100  # Converting to percentage
    sharpe_ratio = performance_high_sharpe[2]
    expected_return =f'{round(expected_return, ndigits=0)}%'
    annual_volatility =f'{round(annual_volatility, ndigits=0)}%'
    sharpe_ratio =f'{round(sharpe_ratio, ndigits=0)}%'

    return {
        "weights": cleaned_weights_high_sharpe,
        "expected_return": expected_return,
        "annual_volatility": annual_volatility,
        "sharpe_ratio": sharpe_ratio
    }