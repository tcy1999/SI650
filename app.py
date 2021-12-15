from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from online_tfidf_bert import IR_bert
from csv2html import csv2html

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
tag_file = 'tag_10_tfidf_2000.csv'
output_file = 'out.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        query = request.form['query']
        return render_template('results.html', query=query)
    else:
        return redirect(url_for('index'), code=302)

@socketio.on('my event')
def generateResults(message):
    query = message['query']
    f_df = IR_bert(tag_file, query)
    f_df.to_csv(output_file, index=False)
    results, count = csv2html(query)
    emit('render', {'results': results, 'count': count})
