FROM continuumio/miniconda3
EXPOSE 8501

COPY . .
RUN conda env create -f demo_environment.yml
SHELL ["conda", "run", "-n", "my-search-engine-demo", "/bin/bash", "-c"]

CMD streamlit run ./my-search-engine-demo/user_interface.py