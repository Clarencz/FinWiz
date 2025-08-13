import numpy as np
import pandas as pd

def calculate_returns(prices:pd.Series)-> pd.Series:
    '''calculates daily returns from a series of prices'''
    return prices.pct_change().dropna()

def calculate_volatility(returns:pd.Series)-> float:
    '''calculates the annualized volatility from a series of daily returns'''
    return returns.std() * np.sqrt(252)#252 trading days ina year

def calculate_sharpe_ratio(returns:pd.Series, risk_free_rate:float = 0.01)->float:
    '''calculate the annualized sharpe ratio'''
    #assuming daily returns and annulizing
    excess_returns = returns - (risk_free_rate / 252)
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)

def calculate_max_drawdown(prices:pd.Series)-> float:
    '''calculate the maximum drawdown of a price series'''
    cumulative_returns = (1+prices.pct_change()).cumprod()
    peak = cumulative_returns.expanding(min_periods = 1).max()
    drawdown = (cumulative_returns - peak)/ peak
    return drawdown.min()