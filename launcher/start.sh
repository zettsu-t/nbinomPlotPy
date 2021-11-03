#!/bin/bash
cd /home/jovyan/streamlit_app
find /home/jovyan/streamlit_app -type f | xargs ls -l
python setup.py bdist_wheel
python -m pip install --no-input dist/nb_plot_streamlit-0.0.1-py3-none-any.whl --force-reinstall
python -m pip install numpy==1.19.5
python -m pip install numba==0.54
yes "" | streamlit run launcher/launch.py
