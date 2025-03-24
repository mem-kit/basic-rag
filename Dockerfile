
FROM ubuntu:22.04

WORKDIR /app

# ENV http_proxy None
# ENV https_proxy None
ENV DEBIAN_FRONTEND noninteractive
ENV BASE_URL_PATH_WEB="/rag"


RUN apt update && apt upgrade -y && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa && apt update && \
    apt install -y python3.12 curl ca-certificates tini 
   ## build-base swig cmake gcc g++ libarrow-dev 

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python3.12 get-pip.py --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org && \
	rm get-pip.py

COPY requirements.txt .

##
RUN pip install  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --upgrade pip setuptools && \
    pip install  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --ignore-installed blinker && \
    pip3 install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org  -r requirements.txt

COPY . .

RUN chmod +x *.sh

EXPOSE 18880

ENTRYPOINT ["tini", "--"]
CMD ["./start.sh"]

## nohup streamlit run streamlit_app.py --server.port 18890 &
## docker build -t streamlit-app:1.0.0 .
## docker run -d -p 18880:18880 --name rai-app streamlit-app:1.0.0



