# nbinomPlotPy

The goal of nbinomPlotPy is to show an example of how to build, test, and deploy a Streamlit app.

## Build and install

``` bash
python setup.py bdist_wheel
python -m pip install dist/nb_plot_streamlit-0.0.1-py3-none-any.whl
```

or in debugging

``` bash
python -m pip install -e .
```

## Example

This is a basic example that shows you how to launch the nbinomPlotPy app:

``` python
from nb_plot_streamlit.ui import draw

def main():
    draw()

if __name__ == '__main__':
    main()
```

## Run this app on Streamlit Server

Execute below on a shell

``` bash
streamlit run launcher/launch.py
```

and you can access the nbinomPlotPy app at <http://example.com:8501/>. Note that you have to replace the URL with an actual server.

The attached `Dockerfile` and `docker-compose.yml` come in handy to make a Docker container to build, test, and run the Streamlit app. See [an introduction to use Python Package Template Project](https://github.com/zettsu-t/create-py-package) for more details.

## Run a headless display

Testing UIs with a headless browser requires a headless display. You can run Xvfb for this purpose. Note that Xvfb runs as root and testing as a user has to share the *DISPLAY* variable and `docker-compose.yml` can hold it.

You can open a shell inside the Docker container

``` bash
docker ps
docker exec -it --user root container-ID /bin/bash
```

and run a headless display as root.

``` bash
export DISPLAY=:99
Xvfb -ac -screen 0 1280x1024x24 "${DISPLAY}" &
```

## Check this app

You can run unit tests, check code, and make documents as a user (jovyan is the default user of jupyter/datascience-notebook).

``` bash
docker exec -it container-ID /bin/bash
```

Notice: this app is not compliant with these checking and documentation yet.

``` bash
export DISPLAY=:99
python -m pip install -e .
yes "" | streamlit run launcher/launch.py &
# Wait until the Streamlit server is ready
ps ux | grep firefox | awk '{print $2}' | xargs kill; pytest
pytest --cov=.
pytest --cov=. --cov-report=html
flake8
pylint src/ tests/
mypy src/nb_plot_streamlit/*.py
sphinx-quickstart
sphinx-build source -b html docs/src
make html
```
