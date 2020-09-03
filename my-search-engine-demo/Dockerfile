FROM python:3.8-slim-buster
EXPOSE 80

COPY . .
RUN pip install -r requirements.txt

RUN mkdir -p ~/.streamlit
RUN cp .streamlit/config.prod.toml ~/.streamlit/config.toml
RUN cp .streamlit/credentials.prod.toml ~/.streamlit/credentials.toml

#Store env variable in container
ARG BUILDTIME_ACS_ENDPOINT
ENV ACS_ENDPOINT=${BUILDTIME_ACS_ENDPOINT}

ARG BUILDTIME_ACS_API_KEY
ENV ACS_API_KEY=${BUILDTIME_ACS_API_KEY}

ARG BUILDTIME_SA_CONN_STR
ENV SA_CONN_STR=${BUILDTIME_SA_CONN_STR}

# RUN conda env create -f demo_environment.yml
# SHELL ["conda", "run", "-n", "my-search-engine-demo", "/bin/bash", "-c"]

CMD streamlit run ./my-search-engine-demo/user_interface.py