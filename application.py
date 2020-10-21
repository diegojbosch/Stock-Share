from flask import Flask, jsonify, request
import requests
from datetime import date, datetime, timedelta
import pytz
from dateutil.relativedelta import relativedelta

application = Flask(__name__)

application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if __name__ == '__main__':
	application.run(debug=True)

with open("token.txt", "r") as file:
	tiingo_api_token = file.readline().strip()
	news_api_token = file.readline().strip()


@application.route('/search')
def homepage():
	return application.send_static_file("index.html")

# retrieve company outlook information
@application.route('/api/v1.0/company-outlook', methods=['GET'])
def get_company_outlook():

	if request.args.get('stock_ticker') is not None:
		stock_ticker = request.args.get('stock_ticker')

	tiingo_api_url = 'https://api.tiingo.com/tiingo/daily/' + stock_ticker + '?token=' + tiingo_api_token

	response = requests.get(tiingo_api_url)
	resp_json = response.json()

	company_outlook = {
		"companyName": resp_json['name'],
		"stockTickerSymbol": resp_json['ticker'],
		"stockExchangeCode": resp_json['exchangeCode'],
		"companyStartDate": resp_json['startDate'],
		"description": resp_json['description']
	}

	return jsonify(company_outlook)


# retrieve stock information for the ticker
@application.route('/api/v1.0/stock-information', methods=['GET'])
def get_stock_information():

	if request.args.get('stock_ticker') is not None:
		stock_ticker = request.args.get('stock_ticker')

	tiingo_api_url = 'https://api.tiingo.com/iex/' + stock_ticker + '?token=' + tiingo_api_token

	response = requests.get(tiingo_api_url)
	resp_json = response.json()

	stock_information = {
		"stockTickerSymbol": resp_json[0]['ticker'],
		"tradingDay": resp_json[0]['timestamp'],
		"previousClosingPrice": resp_json[0]['prevClose'],
		"openingPrice": resp_json[0]['open'],
		"highPrice": resp_json[0]['high'],
		"lowPrice": resp_json[0]['low'],
		"lastPrice": resp_json[0]['last'],
		"change": resp_json[0]['last'] - resp_json[0]['prevClose'],
		"changePercent": ((resp_json[0]['last'] - resp_json[0]['prevClose']) / resp_json[0]['prevClose']) * 100,
		"numberSharesTraded": resp_json[0]['volume']
	}

	return jsonify(stock_information)


# retrieve news articles
@application.route('/api/v1.0/news-articles', methods=['GET'])
def get_news_articles():

	if request.args.get('stock_ticker') is not None:
		stock_ticker = request.args.get('stock_ticker')

	news_api_url = ' https://newsapi.org/v2/everything?apiKey=' + news_api_token + '&q=' + stock_ticker

	response = requests.get(news_api_url)
	resp_json = response.json()

	news_articles = []

	for article in resp_json['articles']:
		news_articles.append({
			"image": article['urlToImage'],
			"title": article['title'],
			"data": article['publishedAt'],
			"linkOriginalPost": article['url']
		})

	return jsonify(news_articles)


@application.route('/api/v1.0/stock-prices', methods=['GET'])
def get_stock_prices():

	if request.args.get('stock_ticker') is not None:
		stock_ticker = request.args.get('stock_ticker')

	six_months_ago = date.today() + relativedelta(months=-6)
	tiingo_api_url = 'https://api.tiingo.com/iex/' + stock_ticker + '/prices?startDate=' + six_months_ago.strftime("%Y-%m-%d") + '&resampleFreq=12hour&columns=open,high,low,close,volume&token=' + tiingo_api_token
	response = requests.get(tiingo_api_url)
	resp_json = response.json()

	data_points = '['
	for data in resp_json:
		d = data['date']
		timestamp = (datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.%fZ') - datetime(1970, 1, 1)).total_seconds()
		data_points += '[' + str(timestamp) + ',' + str(data['close']) + '],'

	data_points = data_points[:-1] + ']'

	# for testing purposes
	#data_points = '[[1317888000000,372.5101],[1317888060000,372.4],[1317888120000,372.16],[1317888180000,371.62],[1317888240000,371.75],[1317888300000,372],[1317888360000,372.22],[1317888420000,372.3],[1317888480000,373.01],[1317888540000,373.36],[1317888600000,373.8],[1317888660000,374.29],[1317888720000,374.05],[1317888780000,374.41],[1317888840000,374.83],[1317888900000,374.81],[1317888960000,375.2],[1317889020000,375.43],[1317889080000,374.94],[1317889140000,375.12],[1317889200000,375.24],[1317889260000,375.16],[1317889320000,374.51],[1317889380000,374.22],[1317889440000,374.69],[1317889500000,374.32],[1317889560000,374.65],[1317889620000,375.13],[1317889680000,375.16],[1317889740000,375],[1317889800000,374.88],[1317889860000,374.41],[1317889920000,374.5],[1317889980000,374.4],[1317890040000,374.86],[1317890100000,375],[1317890160000,375.02],[1317890220000,374.93],[1317890280000,375.75],[1317890340000,376.31],[1317890400000,377.2],[1317890460000,376.75],[1317890520000,376.54],[1317890580000,376.41],[1317890640000,376.46],[1317890700000,376.38],[1317890760000,376.55],[1317890820000,376.45],[1317890880000,376.83],[1317890940000,376.95],[1317891000000,376.1],[1317891060000,375.68]]'

	return data_points

