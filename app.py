from scrape_mars import scrape
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars_data = mongo.db.scrapes.find_one()
    
    if mars_data is None:
        return mars_scraper()
    else:
        return render_template('index.html', scrapes=mars_data)


@app.route('/scrape')
def mars_scraper():
    mars_data = mongo.db.scrapes
    scrape_data = scrape()
    mars_data.update({}, scrape_data, upsert=True)
    time.sleep(15)
    return redirect("/", code=302)
