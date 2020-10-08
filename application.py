from flask import Flask, jsonify, request
import requests

application = Flask(__name__)

if __name__ == '__main__':
	application.run(debug=True)

with open("token.txt", "r") as file:
	tiingo_api_token = file.readline()

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
