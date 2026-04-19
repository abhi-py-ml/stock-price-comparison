import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class StockPriceComparison:
    
    # Get stock data from yfinance
    def get_stock(self, ticker):
        stock = yf.Ticker(ticker)
        data = stock.history(period='max')
        data=data.reset_index()
        data['Date']=pd.to_datetime(data['Date'])
        return data
    
    # Combine data
    def combine_data(self,df1,df2,name1='stock1',name2='stock2'):
        combined=pd.merge(df1,df2,on='Date', suffixes=(f'_{name1}',f'_{name2}'))
        return combined
    
    # Clean Data (Handle missing Values)
    def clean_data(self,data):
        data=data.copy()
        data=data.sort_values('Date').reset_index(drop=True)
        data=data.ffill().bfill()
        return data


    # Normalize Data
    def norm_data(self,combined_data,name1='stock1',name2='stock2'):

        combined_data=combined_data.copy()

        combined_data[f'{name1}_norm']=combined_data[f'Close_{name1}']/combined_data[f'Close_{name1}'].iloc[0]
        combined_data[f'{name2}_norm']=combined_data[f'Close_{name2}']/combined_data[f'Close_{name2}'].iloc[0]
        
        return combined_data
    
    def moving_average(self,combined_data,name1='stock1',name2='stock2'):

        combined_data=combined_data.copy()
        
        combined_data[[f'{name1}_sma20',f'{name2}_sma20']]=combined_data[[f'{name1}_norm',f'{name2}_norm']].rolling(window=20).mean()
        combined_data[[f'{name1}_sma50',f'{name2}_sma50']]=combined_data[[f'{name1}_norm',f'{name2}_norm']].rolling(window=50).mean()

        return combined_data
    
    def plot_graph(self,data,name1='stock1',name2='stock2'):
        fig, axes=plt.subplots(2,1, figsize=(12,8) , sharex=True)

        axes[0].plot(data['Date'],data[f'{name1}_norm'],label=f'{name1} price')
        axes[0].plot(data['Date'],data[f'{name1}_sma20'],label=f'{name1} sma20')
        axes[0].plot(data['Date'],data[f'{name1}_sma50'],label=f'{name1} sma50')
        axes[0].set_title(f'{name1}')
        axes[0].legend()

        axes[1].plot(data['Date'],data[f'{name2}_norm'],label=f'{name2} price')
        axes[1].plot(data['Date'],data[f'{name2}_sma20'],label=f'{name2} sma20')
        axes[1].plot(data['Date'],data[f'{name2}_sma50'],label=f'{name2} sma50')
        axes[1].set_title(f'{name2}')
        axes[1].legend()

        plt.show()
    
    def comparison_graph(self,data,name1='stock1',name2='stock2'):
        

        plt.figure(figsize=(12, 6))

        # Normalized prices
        plt.plot(data['Date'], data[f'{name1}_norm'], label=f'{name1} Price')
        plt.plot(data['Date'], data[f'{name2}_norm'], label=f'{name2} Price')

        # SMA50 
        plt.plot(data['Date'], data[f'{name1}_sma50'], linestyle='--', label=f'{name1} SMA50')
        plt.plot(data['Date'], data[f'{name2}_sma50'], linestyle='--', label=f'{name2} SMA50')

        plt.title('Stock Comparison (Normalized)')
        plt.xlabel('Date')
        plt.ylabel('Normalized Price')
        plt.legend()
        plt.grid(True)
        plt.savefig('comparison.png')

        plt.show()

stock=StockPriceComparison()
tesla=stock.get_stock('TSLA')
apple=stock.get_stock('AAPL')

data=stock.combine_data(tesla,apple,'Tesla','Apple')
cleaned_data=stock.clean_data(data)
normalized_data=stock.norm_data(cleaned_data,'Tesla','Apple')
moving_avg=stock.moving_average(normalized_data,'Tesla','Apple')
stock.plot_graph(moving_avg,'Tesla','Apple')
stock.comparison_graph(moving_avg,'Tesla','Apple')
