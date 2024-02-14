from flask import Flask, render_template, request, jsonify, g

import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = './storage/publications.db'


def get_db():
    """
    Opens a new database connection if there is none yet for the current application context.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
        g.cursor = g.db.cursor()
        # Ensure database is created
        # g.cursor.execute('''CREATE TABLE IF NOT EXISTS publications
        #             (title TEXT PRIMARY KEY, author TEXT, year TEXT, publication_url TEXT)''')
        g.cursor.execute('''
                         CREATE VIRTUAL TABLE IF NOT EXISTS publications 
                    USING FTS5  (title ,author,year, publication_url )
                         ''')

    return g.db, g.cursor


@app.teardown_appcontext
def close_db(error):
    """
    Closes the database again at the end of the request.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    """
    Initialize the database for the app & set the cursor
    """
    db, cursor = get_db()
    return render_template('index.html')


@app.route('/search')
def search():
    # crawler.crawl_and_index()
    query = request.args.get('query', '')
    return searchDocs(query)


def searchDocs(query):
    db, cursor = get_db()
    search_query = f"{query}*"
    print(search_query)
    # Execute the SQL query to search for text in all fields (case-insensitive)
    cursor.execute('''SELECT *,rank FROM publications 
                    WHERE title match ?
                   order by rank desc
                      ''',
                   (search_query,))
    # Fetch the search results
    search_results = cursor.fetchall()
    results = []
    for row in search_results:
        result = dict(row)
        results.append(result)

    return jsonify(results)


app.jinja_env.variable_start_string = '{%'
app.jinja_env.variable_end_string = '%}'
if __name__ == '__main__':
    app.run(debug=True)
