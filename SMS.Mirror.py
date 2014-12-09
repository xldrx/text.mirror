import json
from flask import Flask, render_template, request
import data_adapter

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/master')
def master():
    return render_template('master.html')


@app.route('/get/contacts')
def get_contacts():
    return json.dumps(data_adapter.get_contacts(), indent=4, separators=(',', ': '))

@app.route('/get/overview')
def data():
    return json.dumps(data_adapter.get_overview())

@app.route('/get/locations')
def locations():
    return json.dumps(data_adapter.get_locations())

@app.route('/get/times')
def times():
    return json.dumps(data_adapter.get_times()[1])

@app.route('/get/time_range')
def time_range():
    return json.dumps(data_adapter.get_time_ranges())


def process_args():
    from_date = request.form['from_date'] if 'from_date' in request.form else None
    to_date = request.form['to_date'] if 'to_date' in request.form else None
    include_sends = False if 'include_sends' in request.form and int(request.form['include_sends']) <= 0 else True
    include_recieves = False if 'include_recieves' in request.form and int(
        request.form['include_recieves']) <= 0 else True
    contacts = json.loads(request.form['contacts']) if 'contacts' in request.form else []
    messages = data_adapter.get_messages(include_sends, include_recieves, from_date, to_date, only_from=contacts)
    return messages


@app.route('/get/messages', methods=['POST'])
def get_messages():
    messages = process_args()

    return json.dumps(
        messages, indent=4,
        separators=(',', ': '))

if __name__ == '__main__':
    app.run(debug=True)
