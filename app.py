from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

DATABASE = "terraria_items.db"


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


@app.route("/zenith")
def render_zenith():
    card = run_query("SELECT * FROM weapons WHERE ID IN (415,14,159,167,70,116,43,117, 61,33,29,11,142,327,249, 318, 336, 334, 133)")

    return render_template("zenith_card.html",cards = card)



@app.route("/")
def render_home():
    card = run_query("SELECT * FROM weapons WHERE ID IN (133,568,69)")

    return render_template("home_card.html", cards=card)




@app.route("/data")
def render_data():
    name_search = request.args.get("name", "").strip()
    all_search = request.args.get("all", "").strip()
    type_search = request.args.get("type", "").strip()

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if name_search:
        cursor.execute("""
            SELECT * FROM weapons
            WHERE name LIKE ?

            ORDER BY damage DESC
        """, (f"%{name_search}%",))

    elif all_search:
        cursor.execute("""
            SELECT * FROM weapons

            WHERE name LIKE ?
               OR CAST(damage AS TEXT) LIKE ?
               OR "Damage type" LIKE ?
               OR CAST(Knockback AS TEXT) LIKE ?
               OR CAST("Crit chance" AS TEXT) LIKE ?
               OR "Use time" LIKE ?
               OR Type LIKE ?
               OR Rarity LIKE ?
               OR "Hard Mode" LIKE ?

            ORDER BY damage DESC
        """, (
            f"%{all_search}%",
            f"%{all_search}%",
            f"%{all_search}%",
            f"%{all_search}%",
            f"%{all_search}%",
            f"%{all_search}%",
            f"%{all_search}%",
            f"%{all_search}%",
            f"%{all_search}%"

        ))

    elif type_search:

        cursor.execute("""
            SELECT * FROM weapons

            WHERE type LIKE ?


            ORDER BY damage DESC
        """, (
            f"%{type_search}%",

        ))

    else:
        cursor.execute("SELECT * FROM weapons ORDER BY name")

    cards = cursor.fetchall()
    conn.close()

    return render_template(
        "cards.html",
        cards=cards,
        name_search=name_search,
        all_search=all_search
    )



if __name__ == "__main__":
    app.run(debug=True)
