from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

#create instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)
app.debug = True


# create route that renders index.html template
@app.route("/")
def index():
    mars=mongo.db.news.find_one()
    hemispheres=list(mongo.db.hemispheres.find())
    return render_template("index.html", mars=mars,hemispheres=hemispheres)

@app.route("/scrape")
def scrape():

    # Run the scrape function
    data =mongo.db.news
    data_list=scrape_mars.scrape()
    data.update({},data_list,upsert=True)

    # Redirect back to home page
    return redirect("/",code=302)


if __name__ == "__main__":
    app.run(debug=True)