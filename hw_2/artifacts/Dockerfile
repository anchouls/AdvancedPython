FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends texlive-latex-recommended texlive-fonts-recommended && \
    apt-get install -y --no-install-recommends texlive-latex-extra texlive-fonts-extra texlive-lang-all

COPY .. .

CMD [ "pdflatex", "-output-directory", "shared", "table.tex" ]
