import sqlite3
import logging

from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def delete_sensor_id():
    db = get_db()
    error = None

    try:
        db.execute(
            "DELETE FROM sensor"
        )
        db.commit()
    except Exception as e:
        error = f"Error: Database error deleting sensor_id. {e}"
        logging.warning(error)

    close_db()
    return error


def set_sensor_id(sensor_id):

    # can only handle 1 sensor_id at a time!
    delete_sensor_id()

    db = get_db()
    error = None
    try:
        db.execute(
            "INSERT INTO sensor (sensor_id) VALUES (?)", (sensor_id,)
        )
        db.commit()
    except Exception as e:
        error = f"Error: Database error saving sensor_id: {sensor_id}. {e}"
        logging.warning(error)

    close_db()
    return error


def get_sensor_id():
    db = get_db()
    error = None

    try:
        row = db.execute(
            'SELECT sensor_id FROM sensor'
        ).fetchone()
        sensor_id = row['sensor_id']
    except Exception as e:
        error = f"Error: Database error getting sensor_id. {e}"
        logging.warning(error)
        sensor_id = 0

    close_db()
    return sensor_id
