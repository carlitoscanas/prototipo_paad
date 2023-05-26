# Import libraries
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import json
from datetime import datetime
from scipy.optimize import minimize

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
# Model pipeline
def opt_model_pipe():
    if request.method == 'GET':
        # Extract params from the request payload
        ini_date = request.args.get('ini_date')
        end_date = request.args.get('end_date')
        ticker = request.args.get('ticker')
        if ticker is None:
            ticker = ['AAPL','MSFT','AMZN','TSLA','GOOGL','GOOG','NVDA','BRK-B','META','UNH']
        else:
            ticker = ticker.split(',')
        initial_guess = request.args.get('initial_guess')
        if initial_guess is not None:
            initial_guess = [eval(i) for i in initial_guess.split(',')]
        output_part = request.args.get('output_part')

        # Get stats
        def stats(weights):
            weights = np.array(weights)
            expected_return = np.sum((log_returns.mean()*weights) * 252)
            expected_vol = np.sqrt(np.dot(weights.T,np.dot(log_returns.cov()*252,weights)))
            sharpe_r = expected_return/expected_vol
            return np.array([expected_return,expected_vol,sharpe_r])

        # Minimize negative Sharpe Ratio
        def sr_negate(weights):
            neg_sr = stats(weights)[2] * -1
            return neg_sr

        # Check allocation sums to 1
        def weight_check(weights):
            weights_sum = np.sum(weights)
            return weights_sum - 1

        # Generate input data from data lake
        def get_data(data, ticker=['AAPL','MSFT','AMZN','TSLA','GOOGL','GOOG','NVDA','BRK-B','META','UNH']):
            input_data = pd.DataFrame()
            for i in ticker:
                ticker_adj_close = data[data['Ticker']==i]['Adj Close']
                input_data = pd.concat((input_data,ticker_adj_close),axis=1)
            input_data.columns = ticker
            input_data.sort_index(inplace=True)
            return input_data

        # Generate model params
        def get_params(ticker=['AAPL','MSFT','AMZN','TSLA','GOOGL','GOOG','NVDA','BRK-B','META','UNH']):
            bounds = []
            initial_guess = []
            w = 1 / len(ticker)
            for i in ticker:
                bounds.append((0,1))
                initial_guess.append(w)
            return tuple(bounds), initial_guess
        
        # Extract data from the request payload
        if request.is_json:
            data = request.json
            data = pd.DataFrame(data)
            data.set_index('Date', inplace=True)
            input_data = get_data(data, ticker)
            input_data_msg = 'User data input'
            data_range = 'N/A'
        # Extract data from Data Lake
        else:
            gold = './data/gold/portfolio-optimization/'
            gold_table = 'portfolio_optimization.csv'

            data = pd.read_csv(gold+gold_table)
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)
            
            if ((ini_date is not None) and (end_date is not None)):
                data = data[((data.index>=datetime.strptime(ini_date, '%Y-%m-%d')) & (data.index<=datetime.strptime(end_date, '%Y-%m-%d')))]
                data_range = '{} - {}'.format(ini_date, end_date)
            else:
                ini_date = data.index[0]
                end_date = data.index[-1]
                data_range = '{} - {}'.format(ini_date, end_date)
            
            input_data = get_data(data, ticker)
            input_data_msg = 'Data Lake'

        # Model params
        if initial_guess is None:
            bounds, initial_guess = get_params(ticker)
        else:
            bounds, dummy = get_params(ticker)
        constraints = ({'type':'eq','fun':weight_check})
        
        # Logarithmic return
        log_returns = np.log(input_data/input_data.shift(1))
        
        # Model execution
        results = minimize(sr_negate,initial_guess,method='SLSQP',bounds=bounds,constraints=constraints)
        
        # Portfolio allocation weights and stats
        weights = list(results.x)
        stats = list(stats(results.x))
        
        # Generate JSON output
        if output_part == '0':
            output = {
                'ticker': ticker,
                'weights': weights
            }
        elif output_part == '1':
            output = {
                'return': stats[0],
                'volatility': stats[1],
                'sharpe_ratio': stats[2]
            }
        else:
            output = {
                'ticker': ticker,
                'weights': weights,
                'return': stats[0],
                'volatility': stats[1],
                'sharpe_ratio': stats[2],
                'input_data': input_data_msg,
                'data_range': data_range,
                'message': results.message,
                'success': str(results.success)
            }
        output_json = json.dumps(output)
        
        return jsonify(output_json)
    else:
        return 'This API endpoint expects a GET request.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)