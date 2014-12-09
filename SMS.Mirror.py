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


@app.route('/get/overview', methods=['GET', 'POST'])
def data():
    messages = process_args()
    return json.dumps(data_adapter.get_overview(messages))


@app.route('/get/locations', methods=['GET', 'POST'])
def locations():
    messages = process_args()
    return json.dumps(data_adapter.get_locations(messages))


@app.route('/get/times', methods=['GET', 'POST'])
def times():
    messages = process_args()
    return json.dumps(data_adapter.get_times(messages)[1])


@app.route('/get/time_range', methods=['GET', 'POST'])
def time_range():
    return json.dumps(data_adapter.get_time_ranges())


def process_args():
    args = json.loads(request.data)
    from_date = args['from_date'] if 'from_date' in args  else None
    to_date = args['to_date'] if 'to_date' in args  else None
    include_sends = False if 'include_sends' in args and int(args['include_sends']) <= 0 else True
    include_recieves = False if 'include_recieves' in args and int(
        args['include_recieves']) <= 0 else True
    contacts = json.loads(args['contacts']) if 'contacts' in args  else []
    messages = data_adapter.get_message_list(include_sends, include_recieves, from_date, to_date, only_from=contacts)
    return messages


@app.route('/get/messages', methods=['GET', 'POST'])
def get_messages():
    messages = process_args()

    return json.dumps(
        get_messages(messages), indent=4,
        separators=(',', ': '))


if __name__ == '__main__':
    app.run(debug=True)
