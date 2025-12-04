FROM python:3.12-slim

WORKDIR /locust

COPY . /locust

RUN pip install --no-cache-dir uv && \
    uv sync --no-install-project

EXPOSE 8089

CMD [ "uv", "run", "locust" ]
