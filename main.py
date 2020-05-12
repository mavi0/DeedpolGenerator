from flask import Flask, redirect, url_for, request, render_template, send_file, make_response
from reportlab.pdfgen import canvas
from deedpolgenerator import DeedpolGenerator
import os, io


app = Flask(__name__)

@app.route('/deedpol/<uid>')
def deedpol(uid):
    uid = uid + '.pdf'
    try:
        with open(uid, "rb") as f:
            pdf_b = f.read()
        response = make_response(pdf_b)
        response.headers['Content-Disposition'] = "attachment; filename=deedpoll.pdf"
        response.mimetype = 'application/pdf'
        return response
    finally:
        os.remove("%s" % uid)

@app.route('/witness2', methods=['POST', 'GET'])
def witness2():
    if request.method == 'POST':
        dg = DeedpolGenerator(request.form['oldName'], request.form['newName'], request.form['streetAddress'], request.form['city'], request.form['county'],  request.form['postcode'], request.form['date'])
        dg.generate_deedpol_witness_2()
        return redirect(url_for('deedpol',uid = dg.get_uuid()))
    else:
        return render_template('witness2.html')

@app.route('/witness1', methods=['POST', 'GET'])
def witness1():
    if request.method == 'POST':
        dg = DeedpolGenerator(request.form['oldName'], request.form['newName'], request.form['streetAddress'], request.form['city'], request.form['county'],  request.form['postcode'], request.form['date'])
        dg.generate_deedpol_witness_1()
        return redirect(url_for('deedpol',uid = dg.get_uuid()))
    else:
        return render_template('witness1.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')