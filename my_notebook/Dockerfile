FROM jupyter/datascience-notebook

USER root
RUN apt-get update && apt-get install -y build-essential gnupg2 make patch python3-dev python3-sphinx unzip wget xvfb libegl-dev libpci-dev

RUN wget https://dl.google.com/linux/linux_signing_key.pub
RUN apt-key add linux_signing_key.pub
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -y firefox firefox-geckodriver
RUN wget https://chromedriver.storage.googleapis.com/95.0.4638.17/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/local/bin/

ENV BOOST_VERSION="boost_1_77_0"
RUN wget "https://boostorg.jfrog.io/artifactory/main/release/1.77.0/source/${BOOST_VERSION}.tar.gz"
RUN tar xzf "${BOOST_VERSION}.tar.gz"
RUN cd "${BOOST_VERSION}" && ./bootstrap.sh --with-libraries=python --with-python=python3.9 && ./b2 install cxxflags=-fPIC address-model=64 threading=multi link=static runtime-link=shared variant=release -j4 "--prefix=/opt/${BOOST_VERSION}"
RUN test -d /opt/boost || ln -s "/opt/${BOOST_VERSION}" /opt/boost
RUN test -f "/opt/${BOOST_VERSION}/lib/libboost_python.a" || ln -s "/opt/${BOOST_VERSION}/lib/libboost_python39.a" "/opt/${BOOST_VERSION}/lib/libboost_python.a"

RUN wget https://github.com/google/googletest/archive/refs/heads/main.zip
RUN unzip main.zip
RUN mv googletest-* /opt/googletest

USER jovyan
ENV PATH="/opt/conda/bin:${PATH}"
RUN pip3 install autopep8 check-manifest coverage flake8 matplotlib mypy numpy opencv-python pandas pep8 pipenv pylint pytest pytest-cov pyyaml py_pkg scipy seleniumbase sphinx sphinx_rtd_theme streamlit types-PyYAML types-requests
RUN pip3 install chromedriver-binary-auto

# Same as ports in docker-compose.yml
EXPOSE 8888
EXPOSE 8501

ARG JUPYTER_PASSWORD="sha1:pass-with-build-arg"
RUN sed -E -i.bak -e "s/^[# ]*c.NotebookApp.password *=.*/c.NotebookApp.password = ${JUPYTER_PASSWORD}/" /home/jovyan/.jupyter/jupyter_notebook_config.py
