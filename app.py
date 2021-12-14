from flask import Flask, render_template, request, redirect, url_for
from online_tfidf_bert import IR_bert
from csv2html import csv2html

app = Flask(__name__)
tag_file = 'tag_10_tfidf_2000.csv'
output_file = 'out.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        query = request.form['query']
        f_df = IR_bert(tag_file, query)
        f_df.to_csv(output_file, index=False)
        results, count = csv2html(query)
        return render_template('results.html', query=query, results=results, count=count)
    else:
        return redirect(url_for('index'), code=302)
