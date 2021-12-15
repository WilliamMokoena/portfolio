from flask import Flask, request, jsonify
from flask_cors import CORS
from migration import Migrate, Aggregate
import subprocess
import os
import threading

app = Flask(__name__)
CORS(app)

HOSTNAME = '127.0.0.1'
PORT = 1338


@app.route('/data', methods=['GET'])
def data():
    timespan = request.args.get('timespan')
    data = Migrate(timespan)
    return jsonify(data)


@app.route('/search', methods=['GET'])
def search():
    list_len = request.args.get('list')
    timespan = request.args.get('timespan')
    data = Aggregate(int(list_len), timespan)
    return jsonify(data)


def start_scheduler():
    print('[INFO] Starting scheduler')

    cwd = os.getcwd()
    subprocess.run([f'{cwd}/venv/bin/python3', f'{cwd}/scheduler.py'])


scheduler_thread = threading.Thread(target=start_scheduler)
scheduler_thread.start()

if __name__ == '__main__':
    app.run(host=HOSTNAME, port=PORT)
