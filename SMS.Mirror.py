import json
from flask import Flask, render_template, request
import data_adapter

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/get/contacts')
def get_contacts():
    return json.dumps(data_adapter.get_contacts(), indent=4, separators=(',', ': '))


@app.route('/get/messages', methods=['POST'])
def get_messages():
    from_date = request.form['from_date'] if 'from_date' in request.form else None
    to_date = request.form['to_date'] if 'to_date' in request.form else None

    include_sends = True if 'include_sends' in request.form and int(request.form['include_sends']) > 0 else False
    include_recieves = True if 'include_recieves' in request.form and int(request.form['include_recieves']) > 0 else False
    contacts = json.loads(request.form['contacts']) if 'contacts' in request.form else []

    return json.dumps(
        data_adapter.get_messages(include_sends, include_recieves, from_date, to_date, only_from=contacts), indent=4,
        separators=(',', ': '))

if __name__ == '__main__':
    app.run(debug=True)
