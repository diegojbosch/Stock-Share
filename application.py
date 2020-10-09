from flask import Flask, jsonify, request
import requests

application = Flask(__name__)

if __name__ == '__main__':
	application.run(debug=True)

with open("token.txt", "r") as file:
	tiingo_api_token = file.readline().strip()
	news_api_token = file.readline().strip()

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
