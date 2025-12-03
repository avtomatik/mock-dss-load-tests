# WARNING: Work in Progress. Not Working
FROM python:3.12-slim

WORKDIR /locust

RUN pip install --no-cache-dir uv

COPY pyproject.toml /locust/

RUN uv sync --no-install-project

EXPOSE 8089

# CMD [ "locust", "-f", "/locust/locustfile.py" ]
