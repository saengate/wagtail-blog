[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/saengate/django)](https://github.com/saengate/django/releases/latest)
[![GitHub](https://img.shields.io/github/license/saengate/django)](LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/saengate/django)](https://github.com/saengate/django/graphs/contributors)
[![Build Status](https://travis-ci.org/saengate/django.svg?branch=master)](https://travis-ci.org/saengate/django)

## Descripción django
Plantilla para proyecto django

## Desarrollo

No olvides recargar los paquetes de python en caso de que agregues nuevas librerias.
```sh
poetry lock
```

Puede ejecutar  para facilitar el uso del proyecto:
Para ejecutar el comando debe estar dentro de la carpeta contenedora de cada contanedor.
```sh
./cmdp -h | cmdp -h
```
```sh
-h  | * | --help   muestran los comandos disponibles

-b  | --build           construye el contenedor                         (docker build)
-r  | --run             inicia y accede al contenedor                   (docker run -it)
-rv | --run_v           inicia y accede al contenedor y agrega          (docker exec -it)
                        el volumen para los cambios en ansible
                        tengan efecto inmediato

## VAULT
-ve | --vault_encrypt [ dev | qa | prod ]   Encrypta los valores sensibles del ambiente     (ansible-vault encrypt)
                                            especificado
-vd | --vault_decrypt [ dev | qa | prod ]   Desencrypta los valores sensibles del ambiente  (ansible-vault decrypt)
                                            especificado
-vr | --vault_rekey   [ dev | qa | prod ]   Cambia la llave de encryptación del ambiente    (ansible-vault rekey)
                                            especificado
-vv | --vault_view    [ dev | qa | prod ]   Muestra los valores del ambiente especificado   (ansible-vault view)
```

Dentro del contenedor existen otros comandos que puede facilitar el trabajo del desarrollo, estos son:

```sh
cmdp -h
```
```sh
-h  | * | --help   muestran los comandos disponibles

-rs | --restart-supervisor      Reinicia supervisor y las configuraciones de los programas
-rn | --restart-nginx           Reinicia Nginx
-ra | --restart-all             Reiniciar supervisor las configuraciones de los programas y Nginx
-ca | --create-admin            Crea el usuario administrador por defecto de la aplicación
-t  | --translate               Prepara las traducciones en django
-lp | --log-django             Muestra los logs del projecto y uwsgi
-ls | --log-supervisor          Muestra los logs de supervisor
-lw | --log-websocket           Muestra los logs del websocket
```
      - logproject
      - logsupervisor
      - logwebsocket
      - createadmin
Adicionalmente puedes ejecutar este comando para entrar al entorno virtual del projecto
```sh
source venv
```

## Notas

Este repositorio usa [poetry](https://pypi.org/project/poetry/) para la instalación de sus dependencias.

Se pueden crear distribución pip siguiendo las instrucciones del siguiente [link](https://randomwalk.in/python/bash/2020/01/19/PoetryPackaging.html)

Algunas de los siguientes comandos ya han sido incluidos en el comando "cmd"
Levantar este contenedor especificamente.
```sh
docker build -t  djfullapp .
docker run -p 23:22 -p 8000:80 -p 5050:5555 -p 8001:8080 -it --rm --name djfullapp saengate/djfullapp
```

Levantar contenedor con volumen de ansible y el proyecto
```sh
docker run -v $(pwd)/ansible:/tmp/ansible -v $(pwd):/webapps/django -p 23:22 -p 8000:80 -p 5050:5555 -p 8001:8080 --rm -it --name djfullapp djfullapp
```

Levantar contenedor con volumen de ansible
```sh
docker run -v $(pwd)/ansible:/tmp/ansible -p 23:22 -p 8000:80 -p 5050:5555 -p 8001:8080 --rm -it --name djfullapp djfullapp
```

Para validar que los servicios estan arriba al usar docker
```sh
nmap 0.0.0.0 -p 23,80,5555,8001 | grep -i tcp
```

Para cambiar la clave del vault en Ansible (debe estar parado en esta directorio)
```sh
ansible-vault encrypt ansible/group_vars/develop/vault.yml
ansible-vault decrypt ansible/group_vars/develop/vault.yml
ansible-vault rekey ansible/group_vars/develop/vault.yml
ansible-vault view ansible/group_vars/develop/vault.yml
```
