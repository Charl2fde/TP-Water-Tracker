import psycopg2
from flask import g, current_app
import click
import datetime

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host='localhost',
            database='water',
            user='water',
            password='water')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with db:
        with db.cursor() as cursor:
            with current_app.open_resource('schema.sql') as f:
                cursor.execute(f.read().decode('utf-8'))


@click.command('sample-data')
def sample_data():
    data = (
        (12, datetime.date(2025, 1, 1), 1, 2, 3),
        (13, datetime.date(2025, 1, 2), 1, 2, 3),
        (165, datetime.date(2025, 1, 1), 1, 2, 3),
        (12, datetime.date(2025, 1, 2), 1, 2, 3),
        (165, datetime.date(2025, 1, 2), 1, 2, 3),
    )
    with get_db() as db:
        with db.cursor() as cursor:
            cursor.executemany('INSERT INTO activities  (userid, logday, sleeptime, steps, water) VALUES (%s, %s, %s, %s, %s)', data)
            
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(sample_data)
