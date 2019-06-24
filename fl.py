from flask import Flask, redirect, url_for, request, render_template
from pdflatex import PDFLaTeX
import requests, datetime 

app = Flask(__name__)

def get_latex(url):
    latexRequest = requests.get(url)
    return latexRequest.text

def parse_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()

def number_date(date):
    # day = date.strftime("%d")
    # month = date.strftime("%m")
    # year = date.strftime("%Y")
    # return "%s/%s/%s" % day, month, year
    return date.strftime("%x")

def word_date(date):
    day = int(date.strftime("%d"))
    year = date.strftime("%Y")

    suffix = "th"

    if (day == 1 or day == 21 or day == 31):
        suffix = "st"
    if (day == 2 or day == 22):
        suffix = "nd"
    if (day == 3 or day == 23):
        suffix = "rd"

    print(suffix)

    print("%s %s day of %s in the year %s" % str(day), suffix, date.strftime("%B"), str(year))

    return "%s%s day of %s in the year %s" % str(day), suffix, date.strftime("%B"), str(year)    



def generate_deedpol(oldName, newName, streetAddress, city, county, postcode, date):
    baseLatex = get_latex("https://raw.githubusercontent.com/mavi0/deedpol-template/master/main.tex")
    date = parse_date(date)
    numberDate = number_date(date)
    wordDate = word_date(date)
    print(numberDate)
    print(wordDate)


    


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/generate', methods=['POST', 'GET'])
def login():
    oldName = request.form['oldName']
    newName = request.form['newName']
    streetAddress = request.form['streetAddress']
    city = request.form['city']
    county = request.form['county']
    postcode = request.form['postcode']
    date = request.form['date']

    generate_deedpol(oldName, newName, streetAddress, city, county, postcode, date)
    return redirect(url_for('success',name = oldName))
#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))


@app.route('/')
def index():
   return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
