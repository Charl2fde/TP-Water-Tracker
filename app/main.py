from flask import Blueprint, render_template, request, redirect, url_for
from flask.json import jsonify
from .db import get_db
from .predict import predict_water

bp = Blueprint('main', __name__, url_prefix='')

@bp.route('/', methods=['GET'])
@bp.route('/log', methods=['GET'])
def index():
    return render_template('logactivity.html')

@bp.route('/log', methods=['POST'])
def logactivity():
    userid = request.form['userid']
    logday = request.form['logday']
    water = request.form['water']
    sleeptime = request.form['sleeptime']
    steps = request.form['steps']
    db = get_db()
    with db:
        with db.cursor() as cursor:
            cursor.execute('INSERT INTO activities (userid, logday, sleeptime, steps, water) VALUES (%s, %s, %s, %s, %s)', (userid, logday, water, sleeptime, steps))
    return redirect(url_for('useractivity', userid=userid))

@bp.route('/user/<int:userid>', methods=['GET'])
def useractivity(userid=0):
    activities = []
    with get_db() as db:
        with db.cursor() as cursor:
            cursor.execute('SELECT userid, logday, water, sleeptime, steps FROM activities WHERE userid = %s;', (userid,))
            activities = cursor.fetchall()
    return render_template('useractivity.html', activities=activities, userid=userid)

@bp.route('/user/<int:userid>.json', methods=['GET'])
def useractivityjson(userid=0):
    with get_db() as db:
        with db.cursor() as cursor:
            cursor.execute('SELECT userid, logday, water, sleeptime, steps FROM activities WHERE userid = %s;', (userid,))
            activities = cursor.fetchall()
    return jsonify({'user': userid, 'activities': activities, 'prediction': predict_water()})

