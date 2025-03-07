import os
import urllib.parse
import datetime
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import Flask, request, render_template
load_dotenv()

def create_app():
    app = Flask(__name__)

    
    username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
    password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
    cluster = os.getenv("MONGO_CLUSTER")

    
    mongo_uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"

 
    client = MongoClient(mongo_uri)
    app.db = client.Microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        
        entries = list(app.db.entries.find({}))

        
        entries_with_date = [
            (entry["content"], entry["date"], datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"))
            for entry in app.db.entries.find({})
        ]

        return render_template("home.html", entries=entries_with_date)
    return app

if __name__ == "__main__":
    app.run(debug=True)
