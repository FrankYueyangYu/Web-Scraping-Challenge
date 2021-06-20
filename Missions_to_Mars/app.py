from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    return render_template("index.html", listings=listings)



@app.route("/scrape")
def scraper():
    listings = scrape_mars.scrape()
    mongo.db.listings.update({}, listings, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)