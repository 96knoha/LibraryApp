from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import sqlite3
DATABASE = 'books.db'

app = Flask(__name__)

import db
db.create_books_table()

@app.route('/')
def index():
    con = sqlite3.connect(DATABASE)
    db_books = con.execute('SELECT * FROM books').fetchall()
    con.close

    books = []
    for row in db_books:
        books.append({'title':row[0], 'price':row[1], 'arrival_day':row[2]})

    return render_template(
        'index.html',
        books=books
        )

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/register' , methods=['POST'])
def register():
    title = request.form['title']
    price = request.form['price']
    arrival_day = request.form['arrival_day']

    con = sqlite3.connect(DATABASE)
    con.execute('INSERT INTO books VALUES (?, ?, ?)', 
                (title, price, arrival_day))
    con.commit()
    con.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, 
                        type=int, help='port to listen to')
    args = parser.parse_args()
    port = args.port

    app.config['port'] = port

    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)