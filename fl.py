from flask import Flask, redirect, url_for, request, render_template
from pdflatex import PDFLaTeX
import requests
app = Flask(__name__)

def get_latex(url):
    latex_request = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    print(latex_request.text)

def generate_deedpol(old_name, new_name, street_address, city, county, postcode, date):
    base_latex = get_latex("https://raw.githubusercontent.com/mavi0/deedpol-template/master/main.tex")
    


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/generate', methods=['POST', 'GET'])
def login():
    old_name = request.args.get('oldName')
    new_name = request.form['newName']
    street_address = request.form['streetAddress']
    city = request.form['city']
    county = request.form['county']
    postcode = request.form['postcode']
    date = request.form['date']

    generate_deedpol(old_name, new_name, street_address, city, county, postcode, date)
    return redirect(url_for('success',name = old_name))
#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))


@app.route('/')
def index():
   return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
