FROM nginx:stable as base-develop

RUN apt-get update -q
RUN apt-get install -qy python3-pip python3-venv python3-dev openssh-server openssh-client
RUN apt-get install -qy nano curl supervisor libpq-dev apt-utils gettext apt-utils
RUN pip3 install --upgrade pip
RUN pip3 install ansible virtualenv

# Install and configure SSH
RUN mkdir /var/run/sshd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >>/etc/profile

RUN mkdir -p ~/.ssh
RUN bash -c "ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa 2>/dev/null <<< y >/dev/null"
RUN cat ~/.ssh/id_rsa.pub >>~/.ssh/authorized_keys
RUN chmod og-wx ~/.ssh/authorized_keys

# Install poetry y asegura que se instale el virtual en dentro de `path_venv`variable definida en ansible
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
ENV PATH="$PATH:/root/.poetry/bin"
ENV AIRFLOW_HOME=/usr/local/airflow

WORKDIR /tmp

COPY ./ansible ./ansible
COPY ./pyproject.toml ./
COPY ./ ./django

RUN sed -i 's|#!/usr/bin/env python|#!/usr/bin/env python3|g' ~/.poetry/bin/poetry
RUN poetry export -n --without-hashes -f requirements.txt -o /tmp/requirements.txt --dev

WORKDIR /tmp/ansible
RUN service ssh start && ssh-keyscan -H localhost >>~/.ssh/known_hosts && ansible-playbook config-django.yml
# Directorio del proyecto, debe modificarse si se cambia el directorio original
# Su cambio provocara un fallo en travis
WORKDIR /webapps/django
EXPOSE 22 80 5555 8080 9000

# Se sobreescribe en el docker-compose.yml para ejecutar las migraciones
CMD [ "bash", \
    "-c", \
    "service supervisor start &&    \
        supervisorctl reread &&         \
        supervisorctl update &&         \
        supervisorctl start all &&      \
        service ssh start &&            \
        service nginx start &&          \
        /bin/bash" \
    ]
