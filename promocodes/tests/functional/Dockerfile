FROM python:3.12.8-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/opt/tests'


WORKDIR /opt

COPY tests/functional/requirements.txt /opt/requirements.txt
RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r /opt/requirements.txt

COPY tests/functional/ /opt/tests/functional
COPY tests/src/models/* /opt/tests/models/
COPY tests/src/alembic /opt/alembic
COPY tests/src/alembic.ini /opt/
COPY tests/core /opt/tests/core
COPY tests/utils /opt/tests/utils
COPY tests/src/alembic/env.py /opt/alembic/env.py

RUN mv /opt/tests/functional/conftest.py /opt/tests/conftest.py && \
    mv /opt/tests/functional/fixtures /opt/tests/ && \
    chmod -R 755 /opt/tests

ENTRYPOINT \
  find /opt && \
  python3 tests/utils/wait_for_pg.py && \
  alembic upgrade head && find /opt/ && \
  python3 -m pytest tests -vvv --disable-warnings
