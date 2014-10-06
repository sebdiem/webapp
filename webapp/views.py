from flask import Flask, jsonify, json, g, render_template
import sqlite3

from webapp import app

DB_PATH = 'resources/us-census.db'
TABLE = 'census_learn_sql'
MAX_NUM_OF_VALUES = 100

def set_row_factory():
    db = get_db()
    def my_row_factory(cursor, row):
        keys = ("value", "count", "average age")
        format_c = lambda c: c if not type(c) is float else "%.1f" % c
        return dict([(keys[i], format_c(r)) for i, r in enumerate(row)])
    db.row_factory = my_row_factory

def connect_to_database():
    import os
    return sqlite3.connect(DB_PATH)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/dataiku')
@app.route('/dataiku/index')
def index():
    return render_template("index.html")

@app.route('/dataiku/columns', methods=['GET'])
def get_columns():
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('SELECT * FROM %s' % TABLE) # TODO : insecure?
    r = cursor.fetchone()
    cursor.close()
    return jsonify({'columns': r.keys()})

@app.route('/dataiku/columns/<string:column>', methods=['GET'])
def get_column(column):
    columns = json.loads(get_columns().get_data())['columns']
    if column is None or column not in columns:
        abort(404)
    set_row_factory()
    cursor = get_db().cursor()
    # TODO : the following is insecure according to doc
    query_args = (column, TABLE, column)
    cursor.execute(('SELECT `%s` , COUNT(*) AS `num`, AVG(age) FROM %s '
                    'GROUP BY `%s` ORDER BY num DESC') % query_args)
    result = cursor.fetchall()
    cursor.close()
    return jsonify({'column': result[:MAX_NUM_OF_VALUES],
                    'ignored': max(len(result)-MAX_NUM_OF_VALUES, 0)})

if __name__ == '__main__':
    app.run(debug=True)
