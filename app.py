from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

DATABASE = "terraria.db"


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return None


def run_query(query):
    con = create_connection(DATABASE)

    if con is None:
        return []

    cur = con.cursor()
    cur.execute(query)

    results = cur.fetchall()

    con.close()

    return results


@app.route("/")
def render_home():
    card = run_query("SELECT * FROM weapons WHERE ID IN (3,4,20)")

    return render_template("home_card.html", cards=card)


@app.route("/data")
def render_data():
    cards = run_query("SELECT * FROM weapons")

    return render_template("cards.html", cards=cards)


if __name__ == "__main__":
    app.run(debug=True)
