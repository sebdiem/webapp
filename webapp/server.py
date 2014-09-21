from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import listdir
from os.path import isfile, join, splitext
import json

from urlparse import urlparse, parse_qs
import sqlite3

def get_columns():
    DB.row_factory = sqlite3.Row
    cursor = DB.cursor()
    cursor.execute('SELECT * FROM %s' % TABLE) # TODO : insecure?
    r = cursor.fetchone()
    return r.keys()

def set_row_factory(db):
    def my_row_factory(cursor, row):
        keys = ("column", "count", "average age")
        format_c = lambda c: c if not type(c) is float else "%.1f" % c
        return dict([(keys[i], format_c(r)) for i, r in enumerate(row)])
    db.row_factory = my_row_factory

PORT = 8012
DB = sqlite3.connect('../resources/us-census.db')
TABLE = 'census_learn_sql'
COLUMNS = get_columns()
MAX_NUM_OF_VALUES = 100
set_row_factory(DB)

class MyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")

    def do_GET(self):
        args = parse_qs(urlparse(self.path).query)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        result = []
        request = args.get('request', None)
        if 'columns' in request:
            result  = dict(columns=COLUMNS)
        elif 'data' in request:
            column = args.get('column', None)
            if len(column):
                processed, count_not_processed  = MyHandler.process_request(column[0])
                result = dict(data=processed, ignored=count_not_processed)
        self.wfile.write(json.dumps(result))

    @staticmethod
    def process_request(column):
        """Returns a tuple containing unique values in `column` ordered by count descending, and
        the number of values not included."""
        if column is None or column not in COLUMNS: return [], 0
        
        query_args = (column, TABLE, column)
        cursor = DB.cursor()
        # TODO : following is insecure according to doc
        cursor.execute('SELECT `%s` , COUNT(*) AS `num`, AVG(age) FROM %s GROUP BY `%s` ORDER BY num DESC' % query_args)
        result = cursor.fetchall()
        return result[:MAX_NUM_OF_VALUES], max(len(result)-MAX_NUM_OF_VALUES, 0)


def main():
    try:
        server = HTTPServer(('', PORT), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
