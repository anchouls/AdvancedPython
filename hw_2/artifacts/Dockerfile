FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends texlive-latex-recommended texlive-fonts-recommended && \
    apt-get install -y --no-install-recommends texlive-latex-extra texlive-fonts-extra texlive-lang-all && \
    apt-get install -y graphviz graphviz-dev python3-pygraphviz

COPY main.py .

RUN pip install graphviz
RUN pip install -i https://test.pypi.org/simple/ advpy-ast-tree==1.0.1

CMD python3 main.py shared/table.tex && pdflatex -output-directory shared shared/table.tex
