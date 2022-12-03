"""
Create a function to display top 5 day over day percent moves by absolute value for a number of stocks:
Parameters: tickers – comma delimited list of stock tickers (any valid stock ticker)
range – time range (1 month to 2 years: 1mo,3mo,6mo,1y,2y)

Example: getAnalysis(tickers=”MSFT,F,CMG”, range=”3mo”)
Return Data in JSON format:

URL to get prices / dates:
https://query1.finance.yahoo.com/v7/finance/chart/AAPL?range=3mo&amp;interval=1d&amp;indicators=quote&amp;
includeTimestamps=true
Please note: the API provides prices (use adjQuote values). To calculate day over day percent move,
where day1$ -- day 1 price/ day2$ -- day2 price: 100* (day2$/day1$-1)
Commit your code/configuration
"""
from collections import defaultdict
import datetime
import json
import requests

def topFiveMovers(tickers, rangeOfData):
	"""
	:tickers: List[str]
	:rangeOfData: str
	:rtype: str

	TODO: we can make it more efficient by storing only top 5 moves in a range, by using a different type of 
	a data structure such as heap. However, for below process of getting times of tickers, we need 
	to collect all times before we put together move with related time and then get the top 5 moves, 
	but we might also use indexes of top 5 moves then use that indexing to collect related
	times.  
	"""
	def getMovesOfTicker(): 
		""" 
		helper nested function to return daily percentage moves of a stock
		stores all moves in a range for now
		"""
		moves = []
		for i in range(len(adjclose) -1, -1, -1):
			prev, curr = adjclose[i-1], adjclose[i]
			if not prev or not curr: continue #some tickers'  have null data, so I just skip those !!

			move = ((curr / prev) - 1) * 100
			abs_move = abs(move)
			moves.append((abs_move, move))
		return moves

	def getTimesOfTicker():
		"""
		helper nested function to return daily times of a stock
		stores all times in a range for now
		"""
		times = req.json()['chart']['result'][0]['timestamp']
		formatted_times = []
		for t in times:
			time_format = datetime.datetime.fromtimestamp(t)
			formatted_times.append(time_format)
		return formatted_times

	tickers_and_moves = defaultdict(list) # {ticker: [{date, move}]}
	# make the operations for each ticker in the given ticker array.
	for ticker in tickers:
		url = "https://query1.finance.yahoo.com/v7/finance/chart/{ticker}?interval=1d&range={range}".format(ticker=ticker, range=rangeOfData)
		headers = {'User-agent': 'Mozilla/5.0'}
		req = requests.get(url=url, headers=headers)
		#Please note: the API provides prices (use adjQuote values), hence I used "adjclose" data from API.
		adjclose = req.json()['chart']['result'][0]['indicators']['adjclose'][0]['adjclose'] 
		
		moves, times = getMovesOfTicker(), getTimesOfTicker()
		#put together all moves with times in a given range of a stock.
		moves_and_times = list(zip(moves, times))
		# need to sort in descending order since we need top 5 moves, if used different approach as mentioned above, we won't need to sort it here
		# however, python sort() use TimSort algorithm which is efficient in average.
		moves_and_times.sort(reverse=True)

		#get the top 5 moves
		for i in range(0, 5):
			tickers_and_moves[ticker].append({"date": str(moves_and_times[i][1]), "move": moves_and_times[i][0][1]})

	json_obj = json.dumps(tickers_and_moves)
	return json_obj

if __name__ == "__main__":
	tickers = ["AAPL", "SNAP", "F", "MSFT", "CMG"]
	input_range = "1mo"
	print(topFiveMovers(tickers, input_range))
