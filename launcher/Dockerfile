FROM streamlit

USER root
ARG STREAMLIT_APP_DIR=/home/jovyan/streamlit_app
ARG STREAMLIT_APP_SCRIPT="${STREAMLIT_APP_DIR}/launcher/start.sh"
RUN mkdir -p "${STREAMLIT_APP_DIR}"

COPY config "${STREAMLIT_APP_DIR}/config"
COPY launcher "${STREAMLIT_APP_DIR}/launcher"
COPY patch "${STREAMLIT_APP_DIR}/patch"
COPY src "${STREAMLIT_APP_DIR}/src"
COPY tests "${STREAMLIT_APP_DIR}/tests"
COPY LICENSE.txt "${STREAMLIT_APP_DIR}/"
COPY MANIFEST.in "${STREAMLIT_APP_DIR}/"
COPY pyproject.toml "${STREAMLIT_APP_DIR}/"
COPY README.md "${STREAMLIT_APP_DIR}/"
COPY setup.cfg "${STREAMLIT_APP_DIR}/"
COPY setup.py "${STREAMLIT_APP_DIR}/"

RUN find "${STREAMLIT_APP_DIR}" | xargs chown jovyan:users
RUN chmod ugo+x "${STREAMLIT_APP_SCRIPT}"

EXPOSE 8501

USER jovyan
ENTRYPOINT ["/bin/bash", "/home/jovyan/streamlit_app/launcher/start.sh"]
