FROM python:3.6-stretch

WORKDIR /deedpolgenerator

RUN apt-get update
RUN apt-get install -y texlive-latex-base
RUN pip3 install Flask \
  PDFLaTeX \
  requests \
  gunicorn

COPY . /deedpolgenerator

RUN chmod +x boot.sh

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]