from flask import Flask, jsonify, request
import requests

application = Flask(__name__)

if __name__ == '__main__':
	application.run(debug=True)


#retrieve company outlook information
@application.route('/api/v1.0/company-outlook', methods=['GET'])
def get_company_outlook():

	with open("token.txt", "r") as file:
		tiingo_api_token = file.readline()

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

	print resp_json['description']

	return jsonify(company_outlook)