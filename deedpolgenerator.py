# from pdflatex import PDFLaTeX
from latex import build_pdf
import requests, datetime, shutil, os, glob, uuid

class DeedpolGenerator():
    def __init__(self, old_name, new_name, street_address, city, county, postcode, date):
        self.__uuid = str(uuid.uuid4())
        self.__old_name = old_name.upper()
        self.__new_name = new_name.upper()
        self.__street_address = street_address.capitalize()
        self.__city = city.capitalize()
        self.__county = county.capitalize()
        self.__postcode = postcode.upper()
        self.__date = self.__parse_date(date)

    def __get_latex(self, url):
        latex_request = requests.get(url)
        return latex_request.text

    def __parse_date(self, date):
        return datetime.datetime.strptime(date, "%Y-%m-%d").date()

    def __number_date(self):
        day = self.__date.strftime("%d")
        month = self.__date.strftime("%m")
        year = self.__date.strftime("%Y")
        return str(day) + "/" + str(month) + "/" + str(year)

    def __word_date(self):
        day = int(self.__date.strftime("%d"))
        year = self.__date.strftime("%Y")

        suffix = "th"

        if (day == 1 or day == 21 or day == 31):
            suffix = "st"
        if (day == 2 or day == 22):
            suffix = "nd"
        if (day == 3 or day == 23):
            suffix = "rd"

        w_date = str(day) + suffix + " day of " + self.__date.strftime("%B") + " in the year " +  str(year) 

        return w_date   

    def __generate_latex_vars(self):
        latex_vars = "\\newcommand{\\newname}{" + self.__new_name + "}\n" + "\\newcommand{\\oldname}{" + self.__old_name + "}\n" + "\\newcommand{\\streetaddress}{" + self.__street_address + "}\n" + "\\newcommand{\\city}{" + self.__city + "}\n" + "\\newcommand{\\postcode}{" + self.__postcode + "}\n" + "\\newcommand{\\county}{" + self.__county + "}\n" + "\\newcommand{\\worddate}{" + self.__word_date() + "}\n" + "\\newcommand{\\numberdate}{" + self.__number_date() + "}\n"
        return latex_vars

    def __generate_latex(self, base_latex):
        latex_vars = self.__generate_latex_vars()
        latex = latex_vars + base_latex
        with open("tex/%s.tex" % self.__uuid, "w") as tex:
            tex.write("%s" % latex)

    # def __move_pdf(self):
    #     sourceDir = '/deedpol'
    #     dstDir = 'pdf/'
    #     files = glob.iglob(os.path.join(sourceDir, "*.pdf"))
    #     for file in files:
    #         if os.path.isfile(file):
    #             shutil.move(file, dstDir)
    
    def get_uuid(self):
        return self.__uuid

    def __generate_deedpol(self, base_latex):
        self.__generate_latex(base_latex)
        try:
            os.system('pdflatex tex/%s.tex' % self.__uuid)
        except:
            print("pdf error")
        os.remove("tex/%s.tex" % self.__uuid)
        os.remove("%s.aux" % self.__uuid)
        os.remove("%s.log" % self.__uuid)
        os.remove("%s.out" % self.__uuid)

    def generate_deedpol_witness_2(self):
        base_latex = self.__get_latex("https://raw.githubusercontent.com/mavi0/deedpol-template/master/main.tex")
        self.__generate_deedpol(base_latex)
    
    def generate_deedpol_witness_1(self):
        base_latex = self.__get_latex("https://raw.githubusercontent.com/mavi0/deedpol-template/master/one.tex")
        self.__generate_deedpol(base_latex)
