import datetime

from flask import Flask, redirect, render_template, request, url_for
from mongita import MongitaClientDisk
import requests

app = Flask(__name__)
client = MongitaClientDisk()
db = client.portfolio
investments = db.investments

@app.route("/")
def home():
    trades = investments.find({})
    return render_template("index.html", trades=trades)

@app.route("/new", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("new.html")
    else:
        coin_id = request.form["coin_id"]
        currency = request.form["currency"]
        data = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}").json()
        investments.insert_one({
            "coin_id": coin_id,
            "currency": currency,
            "price": data[coin_id][currency],
            "timestamp": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        }) 
        return redirect(url_for("home"))
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
