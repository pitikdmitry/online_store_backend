FROM python:3.7

RUN echo ' ---> Setting up user environment' \
    && useradd -ms /bin/bash weird_brains_user \
    && mkdir /app \
    && chown weird_brains_user /app

COPY requirements.txt /app

RUN echo ' ---> Installing package dependencies' \
	&& pip install --upgrade pip \
	&& pip install -r /app/requirements.txt

COPY . /app

RUN echo ' ---> Installing package from source' \
    && pip install -e /app

WORKDIR /app

RUN echo ' ---> Clean up build environment' \
    && rm -rf ~/.cache \
    && rm -rf /var/cache/yum \
    && sh -c 'find . | grep -E "(_pycache_|\.pyc|\.pyo$)" | xargs rm -rf'

USER weird_brains_user

CMD ["python3.7", "src.entrypoints.tasks", "--config", "/app/etc/config/development.yml", "server"]
