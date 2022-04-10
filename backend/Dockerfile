FROM tiangolo/uvicorn-gunicorn:python3.9-slim

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


WORKDIR /app

# RUN DEBIAN_FRONTEND=noninteractive apt-get purge -yq git build-essential && \
#     apt-get -yq autoremove && \
#     apt-get clean && \
#     apt-get autoclean && \
#     rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./app /app/app

EXPOSE 8000

CMD ["python","-m","app"]