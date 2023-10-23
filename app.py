

from flask import Flask, jsonify, request

from ariadne import load_schema_from_path, make_executable_schema, QueryType

from graphql_server.flask import GraphQLView
 

app = Flask(__name__)

 

stocks = [

    { 'name': 'S&P 500 Index', 'price': 4224.16, 'ticker': 'SPX' },

    { 'name': 'Crude Oil WTI (NYM $/bbl) Front Month', 'price': 89.02, 'ticker': 'CL.1' },

    { 'name': 'Hang Seng Index', 'price': 17172.13, 'ticker': 'HSI' }

]

dataForStocks = {
    'SPX': {
        'ticker': 'SPX',
        'highest': 4796.56,
        'lowest': 6.90,
        'trading_volume': 2737578858,
        'historical_prices': []
    },
    'CL.1': {
        'ticker': 'CL.1',
        'highest':  147.27,
        'lowest': 11.26,
        'trading_volume': 89368,
        'historical_prices': []
    },
    'HSI': {
        'ticker': 'HSI',
        'highest':  33223.58,
        'lowest': 1894.90,
        'trading_volume':2462206877,
        'historical_prices': []
    },
}

# GET REQUEST (READ)

@app.route('/stocks')

def get_stocks():

    return jsonify(stocks)

 

# POST REQUEST (CREATE)

@app.route('/stock', methods=['POST'])

def add_stock():

    data = request.json

    

    if data.get('name') and data.get('ticker') and data.get('price'):

        stocks.append(

            {

                'name': data.get('name'),

                'ticker': data.get('ticker'),

                'price': data.get('price')

            }

        )

 

        return jsonify({'new_stock': stocks[len(stocks) - 1]})

    

    return jsonify("Missing Data")

type_defs = load_schema_from_path("schema.graphql")
query = QueryType()

schema = make_executable_schema(type_defs, query)

@query.field("dataForStocks")
def resolve_get_dataForStocks(_, info, ticker):
    data_keys = dataForStocks.keys()
    
    # if ticker in data_keys:
    #     return dataForStocks[ticker]
    return dataForStocks[ticker]
        
    return None

app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
