FROM jupyter/datascience-notebook

USER root
RUN apt-get update && apt-get install -y make python3-sphinx gnupg2

RUN wget https://dl.google.com/linux/linux_signing_key.pub
RUN apt-key add linux_signing_key.pub
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update
RUN apt-get install -y google-chrome-stable

USER jovyan
ENV PATH="/opt/conda/bin:${PATH}"
RUN pip3 install autopep8 flake8 mypy pep8 pipenv pylint pytest pytest-cov pyyaml py_pkg seleniumbase sphinx sphinx_rtd_theme types-PyYAML types-requests streamlit

ARG JUPYTER_PASSWORD="sha1:pass-by-build-arg"
RUN sed -i.bak -e "s/^[# ]*c.NotebookApp.password *=.*/c.NotebookApp.password = ${JUPYTER_PASSWORD}/" /home/jovyan/.jupyter/jupyter_notebook_config.py
