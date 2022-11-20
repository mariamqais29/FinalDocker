from flask import Flask
import bitCoin
import redis
import requests
app = Flask(__name__)
btcData = redis.Redis(host='redis', port=6379)

def gitAvgBtCPrice():
    sum=0
    BTCpriceMinute = requests.get('https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USD&limit=9').json()['Data']['Data']
    for bt in BTCpriceMinute:
        sum+=bt['close']
    return (sum/10)


def gitCurBTCPrice(): 
    CurrentBtc = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD').json()['USD']
    return CurrentBtc


@app.route("/")

def home():

    while True:

        price = float("{:.2f}".format(gitCurBTCPrice()))
        avgPrice = float("{:.2f}".format(gitAvgBtCPrice()))

        btcData.set('CurrPrice', price)
        btcData.set('AvgPrice', avgPrice)

        return """
        <meta http-equiv="refresh" content="1" /><h2>Docker Final Task, Current BTC Price</h2><br> <h3>Current BitCoin Price is: {}$</h3><br> <h3>Average BitCoin Price Last 10 Minutes: {}$ </h3><br> """.format(price,avgPrice)
