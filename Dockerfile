FROM nginx:stable as base-develop

RUN apt-get update -q
RUN apt-get install -qy python3-pip python3-venv python3-dev openssh-server openssh-client
RUN apt-get install -qy nano curl supervisor libpq-dev apt-utils gettext apt-utils 
# RUN apt-get install -qy postgresql build-essential gcc postgresql-contrib
RUN apt-get install -qy git groff gnupg2
RUN pip3 install --upgrade pip
RUN pip3 install ansible==2.9 virtualenv

# Oh my zsh
RUN apt-get install zsh -qy
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
RUN git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
RUN sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="powerlevel10k\/powerlevel10k"/' ~/.zshrc

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

WORKDIR /tmp

COPY ./ansible ./ansible
COPY ./pyproject.toml ./
COPY ./ ./wagtailblog

RUN sed -i 's|#!/usr/bin/env python|#!/usr/bin/env python3|g' ~/.poetry/bin/poetry
# RUN poetry lock --no-update
# RUN poetry export -n --without-hashes -f requirements.txt -o /tmp/requirements.txt --dev

WORKDIR /tmp/ansible
ARG ANSIBLE_KEY
ENV ANSIBLE_KEY=$ANSIBLE_KEY
RUN touch /tmp/ansible/.key
RUN echo $ANSIBLE_KEY >> /tmp/ansible/.key
RUN cat /tmp/ansible/.key
# RUN service ssh start && ssh-keyscan -H localhost >>~/.ssh/known_hosts && ansible-playbook config-django.yml

# Change UTC
ENV TZ="America/Santiago"

# INIT AWS config credentials
ARG AWS_ACCESS
ARG AWS_SECRET
ARG AWS_REGION

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET
ENV AWS_DEFAULT_REGION=$AWS_REGION

RUN mkdir -p /root/.aws

RUN echo "[default]" >> /root/.aws/credentials
RUN echo "aws_access_key_id=${AWS_ACCESS}" >> /root/.aws/credentials
RUN echo "aws_secret_access_key=${AWS_SECRET}" >> /root/.aws/credentials

RUN echo "[default]" >> /root/.aws/config
RUN echo "region=${AWS_REGION}" >> /root/.aws/config
RUN echo "output=json" >> /root/.aws/config

RUN cat /root/.aws/config
RUN cat /root/.aws/credentials

RUN chmod 600 /root/.aws/*
# END AWS config credentials

# Directorio del proyecto, debe modificarse si se cambia el directorio original
# Su cambio provocara un fallo en travis
WORKDIR /webapps/wagtailblog
EXPOSE 80 7000 7001 7002

# Se sobreescribe en el docker-compose.yml para ejecutar las migraciones
CMD [ "zsh"]
