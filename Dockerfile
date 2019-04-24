FROM python:3.6

RUN echo ' ---> Setting up user environment' \
    && useradd -ms /bin/bash weird_brains_user \
    && mkdir /app \
    && chown weird_brains_user /app

# setting timezone
ARG TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt /app

RUN echo ' ---> Installing package dependencies' \
	&& pip install --upgrade pip \
	&& pip install -r /app/requirements.txt

COPY . /app

RUN echo ' ---> Installing package from source' \
    && pip install -e /app

# give user rights
#RUN chown -R weird_brains_user:weird_brains_user /app
#RUN chmod 777 /app
#RUN cd /app && mkdir static || true

WORKDIR /app

RUN echo ' ---> Clean up build environment' \
    && rm -rf ~/.cache \
    && rm -rf /var/cache/yum \
    && sh -c 'find . | grep -E "(_pycache_|\.pyc|\.pyo$)" | xargs rm -rf'

#USER weird_brains_user

CMD sleep 20 && python3.6 src/tasks.py --config /app/etc/config/production.yml server
