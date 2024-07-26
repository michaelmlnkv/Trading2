# Trading
The idea of this project is to use various stochastic methods to:
- Find pairs (for now) of stocks that historically have the same trends
    - What is the optimal time window for this? Guess we'll find out.
    - 'The same trend' is a pair of stocks which reject the hypothesis test: 'Two stocks, S1 and S2, are cointegrated' with a p-value < 0.05.
    - This idea should be expanded to incorporate more than one stock (basket of assets)
    - Look into diversifying trading signals
- Introduce parts of the Black-Scholes equation such as GBM (Geometric Brownian Motion) to model the behaviour of stocks in a certain timeframe
    - We need to select this timeframe in a probabilistically feasible manner to ensure that the results are to have any sort of significance
- Combine the two above parts to create a model which can (semi)-reliably provide trading signals
    - Potentially identify pairs which might trend the same in the future
    - Backtest the shit out of it
    - Try to apply it in real time?
- Find similar stocks using KNN and discrete time analysis
- Model various options payoffs, taking into account Black-Scholes and the Greeks
So far achieved:
- pairsTrading:
    - 
