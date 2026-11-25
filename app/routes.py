import sqlite3
from flask import Flask, jsonify, render_template
from app.database import DB_PATH, initialize_database

app = Flask(__name__)


def connection():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


@app.get('/')
def dashboard():
    return render_template('dashboard.html')


@app.get('/api/stats')
def stats():
    with connection() as db:
        total = db.execute('SELECT COUNT(*) FROM alerts').fetchone()[0]
        severity = {str(r['severity']): r['n'] for r in db.execute(
            'SELECT severity, COUNT(*) AS n FROM alerts GROUP BY severity')}
        protocols = [dict(r) for r in db.execute(
            "SELECT COALESCE(protocol, 'Unknown') AS name, COUNT(*) AS value "
            'FROM alerts GROUP BY protocol ORDER BY value DESC')]
        categories = [dict(r) for r in db.execute(
            "SELECT COALESCE(signature, 'Unknown') AS name, COUNT(*) AS value "
            'FROM alerts GROUP BY signature ORDER BY value DESC LIMIT 8')]
        timeline = [dict(r) for r in db.execute(
            "SELECT substr(timestamp, 1, 16) AS bucket, COUNT(*) AS value "
            'FROM alerts GROUP BY bucket ORDER BY bucket DESC LIMIT 20')]
    return jsonify(total=total, high=severity.get('1', 0),
                   medium=severity.get('2', 0),
                   low=sum(n for key, n in severity.items() if key not in ('1', '2')),
                   protocols=protocols, categories=categories,
                   timeline=list(reversed(timeline)))


@app.get('/api/alerts')
def alerts():
    with connection() as db:
        rows = db.execute('SELECT * FROM alerts ORDER BY id DESC LIMIT 500').fetchall()
    return jsonify([dict(row) for row in rows])


if __name__ == '__main__':
    initialize_database()
    app.run(host='127.0.0.1', port=5000, debug=False)
