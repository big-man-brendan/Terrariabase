from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "yugioh.db"


def create_connection(db_file):
    """
    Creates a connection to the database
    :parameter db_file - the name of the file
    :returns   connection - a connection to the database
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


def run_query(query):
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    con.close()
    return results


@app.route('/')
def render_home():
    cards = run_query("SELECT * FROM tbl_cards")

    return render_template("cards.html", cards=cards)


if __name__ == '__main__':
    app.run()
