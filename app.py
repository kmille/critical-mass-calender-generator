from flask import Flask, jsonify
from flask_mysqldb import MySQL
from ipdb import set_trace
import os

app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "toor"
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT city FROM mass.locations""")
    rv = cur.fetchall()
    set_trace()
    return jsonify([x[0] for x in rv])


if __name__ == '__main__':
    app.run(debug=True)
