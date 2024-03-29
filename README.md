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
## Dockerfile

 El archivo dockerfile usa entre sus herramientas de instalación `ansible`, dentro de la carpeta del mismo nombre encontrará el archivo [readme](ansible/readme.md) con el detalle de como usar esta herramienta, toda su estructura e información sobre la carpeta. Puedes usar esta información en caso de necesitar modificar la imagen y esta modificación resulte compleja de realizar directamente en docker o toque alguno de los archvios de configuración que se encuentran entre las plantillas, `ansible` -> `roles` -> `ansible-role-django` -> `templates`.


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
docker run -v $(pwd)/ansible:/tmp/ansible -v $(pwd):/webapps/wagtailblog -p 23:22 -p 8000:80 -p 5050:5555 -p 8001:8080 --rm -it --name djfullapp djfullapp
```

Levantar contenedor con volumen de ansible
```sh
docker run -v $(pwd)/ansible:/tmp/ansible -p 23:22 -p 8000:80 -p 5050:5555 -p 8001:8080 --rm -it --name djfullapp djfullapp
```

docker build --build-arg AWS_ACCESS=$AWS_ACCESS --build-arg AWS_SECRET=$AWS_SECRET --build-arg AWS_REGION=$AWS_REGION --build-arg ANSIBLE_KEY=$ANSIBLE_KEY  --no-cache -t django .

docker run -e SECRET_KEY=${SECRET_KEY} -v $(pwd)/ansible:/tmp/ansible --rm -it --name django django bash
docker run -e SECRET_KEY=${SECRET_KEY} --rm -it --name django django bash -c "source /opt/venv/bin/activate && ./manage.py test";


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

Shell
```sh
./manage.py shell_plus --notebook
```

Debe existir un bucket en AWS S3
Debes crear en VPC un endpoint para el servicio de S3
# Deploy commands
https://github.com/Miserlou/Zappa#advanced-usage

* poetry lock --no-update
* poetry export -n --without-hashes -f requirements.txt -o requirements.txt

* `zappa deploy production` firts deploy in web

* `zappa update production` update web

## Migrations

* `zappa manage production migrate`



# https://aws.amazon.com/es/getting-started/hands-on/configure-connect-serverless-mysql-database-aurora/

https://us-east-1.console.aws.amazon.com/cloud9/ide/62871adac73d4c8a80b65d51d776f488

mysql --user=[your Master username] --password -h [your database endpoint]

DATABASE_HOST	wagtail.czdeyx0up9tn.us-east-1.rds.amazonaws.com
DATABASE_NAME	wagtaildb_prod
DATABASE_PASSWORD	PG5432.4dm1n-U$ER:P4ss
DATABASE_PORT	5432
DATABASE_USER	saengate_db
ENV	production
REDIS_HOST	redis.neby3x.0001.use1.cache.amazonaws.com:6379


aun no se si esto es util para zappa.
AWS
https://www.codingforentrepreneurs.com/blog/aws-iam-user-role-policies-zappa-serverless-python


https://www.codingforentrepreneurs.com/blog/serverless-django-with-zappa-on-aws-lambda

primero se despliega y luego se agregan los grupos de seguridad y se actualiza
zappa deploy production

"vpc_config" : {
      "SubnetIds": ["subnet-d742dcd9"],
      "SecurityGroupIds": [ "sg-0c277a37", "sg-09b054a57f1046265", "sg-0a72fc102701838e8", "sg-08459b51386be4d6b" ]
},
Esto esta en prueba desde el 04-01-2021, para validar si en efecto reduce los costos.
"keep_warm": false, luego hacer `zappa unschedule production` Evita que zappa haga solicitudes constantes a la función para mantenerla viva, esto reduce el coste de AWS pero hace que la función tarde en responder.
Recomiendo revisar el link para reducir costos:
https://aws.amazon.com/es/blogs/aws-spanish/10-cosas-que-puede-hacer-hoy-para-reducir-los-costos-de-aws/
Hay problemas con el permiso en el rol que no permite agregarlo en el zappa hasta agregarlo directamente en las configuraciones de la función lambda. Puede que haga falta revisar los permisos que hacen falta agregar a alguno de los roles para resolver esto en el deploy o el update si esta la configuración voc_config: 

"""
botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the UpdateFunctionConfiguration operation: Your access has been denied by EC2, please make sure your request credentials have permission to DescribeSecurityGroups for sg-0c277a37,sg-09b054a57f1046265,sg-0a72fc102701838e8,sg-08459b51386be4d6b. EC2 Error Code: UnauthorizedOperation. EC2 Error Message: You are not authorized to perform this operation.
"""

zappa update production
zappa manage production "collectstatic --no-input"
zappa manage production "migrate --no-input"
zappa tail production
zappa status production

zappa undeploy production --remove-logs





https://stackoverflow.com/questions/19331497/set-environment-variables-from-file-of-key-value-pairs/19331521


En local:
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user('saengate', 'saengate@gmail.com', 'saengate')" | ./manage.py shell
En producción:
zappa invoke --raw production "from django.contrib.auth.models import User; User.objects.create_superuser('saengate', 'saengate@gmail.com', 'secret-password')";
zappa invoke --raw production "from django.contrib.auth.models import User; User.objects.create_superuser('contact', 'contact@saengate.com', 'secret-password')"


Modificar el fixture para que el usuario coincida
"user": [
"saengate"
]

"owner": [
"saengate"
],

zappa manage production "loaddata ./fixtures/data.json"


