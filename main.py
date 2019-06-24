from flask import Flask, redirect, url_for, request, render_template, send_file
from pdflatex import PDFLaTeX
import requests, datetime, shutil, os, glob, uuid

app = Flask(__name__)

def get_latex(url):
    latexRequest = requests.get(url)
    return latexRequest.text

def parse_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()

def number_date(date):
    day = date.strftime("%d")
    month = date.strftime("%m")
    year = date.strftime("%Y")
    return str(day) + "/" + str(month) + "/" + str(year)

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

    wDate = str(day) + suffix + " day of " + date.strftime("%B") + " in the year " +  str(year) 

    return wDate   

def generate_latex_vars(oldName, newName, streetAddress, city, county, postcode, numberDate, wordDate):
    latexVars = "\\newcommand{\\newname}{" + newName + "}\n" + "\\newcommand{\\oldname}{" + oldName + "}\n" + "\\newcommand{\\streetaddress}{" + streetAddress + "}\n" + "\\newcommand{\\city}{" + city + "}\n" + "\\newcommand{\\postcode}{" + postcode + "}\n" + "\\newcommand{\\county}{" + county + "}\n" + "\\newcommand{\\worddate}{" + wordDate + "}\n" + "\\newcommand{\\numberdate}{" + numberDate + "}\n"
    return latexVars

def generate_latex(oldName, newName, streetAddress, city, county, postcode, date, uid):
    baseLatex = get_latex("https://raw.githubusercontent.com/mavi0/deedpol-template/master/main.tex")
    date = parse_date(date)
    numberDate = number_date(date)
    wordDate = word_date(date)
    latexVars = generate_latex_vars(oldName, newName, streetAddress, city, county, postcode, numberDate, wordDate)
    latex = latexVars + baseLatex
    with open("tex/%s.tex" % uid, "w") as tex:
        tex.write("%s" % latex)

def move_pdf():
    sourceDir = '.'
    dstDir = 'pdf/'
    files = glob.iglob(os.path.join(sourceDir, "*.pdf"))
    for file in files:
        if os.path.isfile(file):
            shutil.move(file, dstDir)


def generate_deedpol(oldName, newName, streetAddress, city, county, postcode, date, uid):
    generate_latex(oldName, newName, streetAddress, city, county, postcode, date, uid)
    pdfl = PDFLaTeX.from_texfile('tex/%s.tex' % uid)
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
    move_pdf()
    os.remove("tex/%s.tex" % uid)

@app.route('/deedpol/<uid>')
def deedpol(uid):
    try:
        return send_file('pdf/%s.pdf' % uid, attachment_filename='deedpol.pdf')
    finally:
        os.remove("pdf/%s.pdf" % uid)


@app.route('/generate', methods=['POST', 'GET'])
def generate():
    oldName = request.form['oldName'].upper()
    newName = request.form['newName'].upper()
    streetAddress = request.form['streetAddress'].capitalize()
    city = request.form['city'].capitalize()
    county = request.form['county'].capitalize()
    postcode = request.form['postcode'].upper()
    date = request.form['date']
    uid = str(uuid.uuid4())

    generate_deedpol(oldName, newName, streetAddress, city, county, postcode, date, uid)
    return redirect(url_for('deedpol',uid = uid))

@app.route('/')
def index():
   return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
