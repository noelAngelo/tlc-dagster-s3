FROM python:3.11-slim

ENV DAGSTER_HOME=/opt/dagster/dagster_home/
ENV DAGSTER_PG_USERNAME=dagster
ENV DAGSTER_PG_PASSWORD=dagster
ENV DAGSTER_PG_HOST=postgres
ENV DAGSTER_PG_DB=dagster

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app
RUN pip install dagster-webserver dagster-postgres dagster-aws pyarrow pandas beautifulsoup4 s3fs

# Copy dagster instance YAML to $DAGSTER_HOME
COPY dagster.yaml /opt/dagster/dagster_home/

WORKDIR /opt/dagster/app
COPY workspace.yaml .





