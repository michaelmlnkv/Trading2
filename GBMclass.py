import datetime
import yfinance as yf
import statsmodels.tsa.stattools as sm
import seaborn
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class GBMpredictor:
    def __init__(self, stock: str) -> None:
        self.stock = stock
        self.dataCollector = dataCollection()
        self.grapher = Grapher()
        self.dt = 1
        self.sim = []
        self.final_pred = pd.DataFrame()
    
    def getData(self, start_date, end_date):
        self.start = start_date
        self.end = end_date
        return self.dataCollector.getData(stock=self.stock, start_date=self.start, end_date=self.end, attribute='Close')


    def runSim(self, start_date, end_date, sim_start, sim_end, iterations):
        self.train_start = start_date
        self.train_end = end_date
        self.sim_start = sim_start
        self.sim_end = sim_end
        self.iterations = iterations

        self.train_data = self.getData(self.train_start, self.train_end)
        self.test_data = self.getData(self.sim_start, self.sim_end)
        self.calculations(self.train_data)
        self.N = len(self.test_data)
        
        for _ in range(self.iterations):
            self.indSim()

        self.final_pred['real'] = self.test_data
        self.final_pred['simulated'] = self.makeFinalCalc()

        self.grapher.drawGraph(self.sim, 'Monte Carlo Sim', 'Price (USD)', 'Time')
        self.grapher.drawGraph(data=[self.final_pred['real'], self.final_pred['simulated']], name='Real vs Predicted Price', ylabel=
                               'Price (USD)', xlabel='Time')

    
    def indSim(self):
        self.s0 = self.train_data.iloc[-1]
        S = [self.s0]
        for t in range(self.N):
            rand_var = np.random.normal(0,1)
            S.append(S[-1] * np.exp(self.drift + self.sigma * rand_var))
        S = S[:len(S)-1]
        S = pd.Series(S, index=self.test_data.index)
        self.sim.append(S)


    def calculations(self, data):
        self.daily_returns = ((data / data.shift(1)) - 1)[1:]
        self.mu = np.mean(self.daily_returns)
        self.sigma = np.std(self.daily_returns)
        self.drift = self.mu - 0.5 * self.sigma ** 2

    def makeFinalCalc(self):
        maxes = []
        mins = []

        for i in range(self.N):
            daylist = []
            for j in range(self.iterations):
                daylist.append(self.sim[j].iloc[i])
            
            maxes.append(max(daylist))
            mins.append(min(daylist))

        return np.array(maxes) * 0.5 + np.array(mins) * 0.5





class dataCollection:
    def __init__(self) -> None:
        pass
    
    def getData(self, stock, start_date, end_date, attribute):
        self.stock = stock
        self.start = start_date
        self.end = end_date
        self.attribute = attribute
        self.ticker = yf.Ticker(stock)

        return self.ticker.history(start=self.start, end=self.end)[self.attribute]
    

class Grapher:
    def __init__(self) -> None:
        pass

    def drawGraph(self, data, name, ylabel, xlabel):
        plt.figure(figsize=(12,6))
        plt.title(name)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

        for i in data:
            plt.plot(i)
        
        plt.show()

        
    

simulation = GBMpredictor('aapl')
simulation.runSim(start_date='2022-01-01', end_date='2024-08-02', sim_start='2024-08-01', sim_end='2024-08-08', iterations=10000)
