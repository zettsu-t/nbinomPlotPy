"""
A Streamlit UI
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import yaml
from .nbinom import NbinomDist

X_STEP = 32.0
DEFAULT_CSV_FILENAME = "density.csv"
DEFAULT_CSV_MIME = "text/csv"


def read_default_config() -> dict:
    """
    Read a default config in the config file

    :rtype: dict
    :return: Returns the default config
    """

    with open(file="config/config.yml", mode='r', encoding='utf8') as file:
        default_config: dict = yaml.safe_load(file)["default"]
    return default_config


def draw():
    """Draw a negative binomial distribution"""

    # Initialize once
    if "nb" not in st.session_state:
        default_config: dict = read_default_config()
        max_nbinom_size: float = default_config["default_max_nbinom_size"]
        st.session_state["default_max_nbinom_size"] = max_nbinom_size
        nbinom_dist = NbinomDist(initial_values=default_config)
        nbinom_dist.set_x_step(1.0 / X_STEP)
        st.session_state["nb"] = nbinom_dist

    st.title("Negative binomial distribution")
    state = st.session_state["nb"]

    size = st.sidebar.slider(
        "Size",
        min_value=0.0,
        max_value=np.max([np.ceil(state.get_size() * 2.0),
                          st.session_state["default_max_nbinom_size"]]),
        value=state.get_size(),
        step=1.0
    )

    prob = st.sidebar.slider(
        "Prob",
        min_value=0.0,
        max_value=1.0,
        value=state.get_prob(),
        step=0.05
    )

    mu = st.sidebar.number_input(
        "Mu",
        value=state.get_mu(),
        step=1.0
    )

    selector = st.sidebar.radio("Fix", ["size", "mu"])

    def update_size_prob():
        if selector == "size":
            state.update_size_prob(size, prob)
        elif selector == "mu":
            state.update_mu_prob(mu, prob)
        else:
            raise ValueError("Unexpected selection!")

    st.sidebar.button("Update", on_click=update_size_prob)

    quantiles = ["0.99", "0.999", "0.9999"]
    quantile = st.sidebar.selectbox(
        "Quantile",
        options=quantiles
    )

    if quantile != state.get_quantile():
        state.set_quantile(quantile)

    st.sidebar.button(
        "Reset",
        on_click=state.reset
    )

    xs, ys = state.get_data()
    fig, ax = plt.subplots()
    ax.plot(xs, ys)
    st.pyplot(fig)

    csv = state.get_df()
    st.download_button(label="download",
                       data=csv,
                       file_name=DEFAULT_CSV_FILENAME,
                       mime=DEFAULT_CSV_MIME)
