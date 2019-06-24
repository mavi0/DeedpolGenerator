from flask import Flask, redirect, url_for, request
from pdflatex import PDFLaTeX
import urllib.request
app = Flask(__name__)

def generate_deedpol(old_name, new_name, street_address, city, county, postcode, date):
    base_latex = urllib.request.urlopen("https://raw.githubusercontent.com/mavi0/deedpol-template/master/main.tex")


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/generate', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        old_name = request.form['oldName']
        new_name = request.form['newName']
        street_address = request.form['streetAddress']
        city = request.form['city']
        county = request.form['county']
        postcode = request.form['postcode']
        date = request.form['date']

        generate_deedpol(old_name, new_name, street_address, city, county, postcode, date)

     #   return redirect(url_for('success',name = user))
#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))


if __name__ == '__main__':
    app.run(debug=True)
